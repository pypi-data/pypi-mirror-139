import multiprocessing as mp
from threading import Semaphore, Lock
from stonewave.sql.udtfs.logger import logger
import os

DEFAULT_POOL_SIZE = int(os.getenv("STONEWAVE_PY_TABLE_FUNC_POOL_SIZE", 16))


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class TaskManager(object):
    # ideally the pool_size can be controlled by a config variable
    def __init__(self, pool_size=DEFAULT_POOL_SIZE):
        self._reset(pool_size=pool_size)

    ## add a reset function used in unit test for this singleton object, mock reinitilization of TaskManager
    def _reset(self, pool_size=mp.cpu_count()):
        if hasattr(self, "_pool"):
            self._pool.close()
            self._pool.terminate()
        logger.info("init worker pool", pool_size=pool_size)
        # TODO change max_limit to a configuarable constant
        self.max_limit = 32
        self.max_pool_size = pool_size
        self._pool = mp.Pool(processes=pool_size)
        self.workers = Semaphore(pool_size)
        # ensures the semaphore is not replaced while used
        self.workers_mutex = Lock()
        manager = mp.Manager()
        self.queues = []
        for i in range(pool_size):
            send_queue = manager.Queue()
            recv_queue = manager.Queue()
            self.queues.append([False, (send_queue, recv_queue)])

    def get_pool(self):
        return self._pool

    def change_pool_size(self, new_size):
        """Set the Pool to a new size."""
        logger.info("change task manager pool size")
        with self.workers_mutex:
            if new_size > self.max_limit or new_size <= 0:
                logger.error("new pool size not in the range of 0 and cpu count size")
                return False
            current_value = self.workers._value
            diff_value = new_size - self.max_pool_size
            value = current_value + diff_value
            if value < 0:
                logger.error(
                    "pool workers still running, semaphore value can not be negative", changed_semaphore_value=value
                )
                return False
            self.workers = Semaphore(value)
            self.max_pool_size = new_size
            for i in range(diff_value):
                send_queue = mp.Manager().Queue()
                recv_queue = mp.Manager().Queue()
                self.queues.append([False, (send_queue, recv_queue)])
            return True
        return False

    def new_task(self, task, func_name):
        """Start a new task, blocks if queue is full."""
        with self.workers_mutex:
            if not self.workers.acquire(blocking=False):
                return ((None, None, None), False)
            (index, send_queue, recv_queue) = self._acquire_queues()
            if index is None or send_queue is None or recv_queue is None:
                return ((None, None, None), False)

        args = (
            func_name,
            send_queue,
            recv_queue,
        )
        result = self._pool.apply_async(task, args=args, callback=self.task_done)
        return ((index, send_queue, recv_queue), result)

    def _acquire_queues(self):
        for i in range(len(self.queues)):
            item = self.queues[i]
            # check first item as dirty bit
            if item[0] == False:
                (send_queue, recv_queue) = item[1]
                if send_queue.qsize() != 0 or recv_queue.qsize() != 0:
                    logger.error("queue is dirty", queueno=i)
                    manager = mp.Manager()
                    send_queue = manager.Queue()
                    recv_queue = manager.Queue()
                    item[1] = (send_queue, recv_queue)
                item[0] = True
                return (str(i), send_queue, recv_queue)

        return (None, None, None)

    def get_queues(self, index):
        index = int(index)
        with self.workers_mutex:
            item = self.queues[index]
            if item[0] == False:
                return (None, None)
            return item[1]

    def release_queues(self, index):
        index = int(index)
        with self.workers_mutex:
            item = self.queues[index]
            if item[0] == False:
                logger.info("queues already released", index=index)
            else:
                (send_queue, recv_queue) = item[1]
                if send_queue.qsize() != 0 or recv_queue.qsize() != 0:
                    logger.error("queue is dirty", queueno=index)
                    manager = mp.Manager()
                    send_queue = manager.Queue()
                    recv_queue = manager.Queue()
                    item[1] = (send_queue, recv_queue)
                item[0] = False

    def task_done(self, *args, **kwargs):
        """Called once task is done, releases the queue is blocked."""
        with self.workers_mutex:
            print("task done")
            logger.debug("function execution task done")
            self.workers.release()
