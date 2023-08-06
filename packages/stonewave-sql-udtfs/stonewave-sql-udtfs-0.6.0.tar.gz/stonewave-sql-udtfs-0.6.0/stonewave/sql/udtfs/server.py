from fastapi import FastAPI, HTTPException
import multiprocessing as mp
from numpy import block
from pydantic import BaseModel, Json
from typing import Optional
from stonewave.sql.udtfs.task_manager import TaskManager
import uvicorn
import asyncio
import stonewave.sql.udtfs.function_executor as function_executor
from stonewave.sql.udtfs.logger import logger, get_logger_config
import json

app = FastAPI()


class RequestObj(BaseModel):
    func_name: Optional[str] = None
    method: str
    params: Json
    execution_id: Optional[int] = None

    class Config:
        schema_extra = {"example": {"func_name": "faker", "method": "eval", "params": {}}}


@app.post("/table-functions/execs")
async def create(req: RequestObj):
    try:
        func_name = req.func_name
        # acquire resources from task manager
        task_manager = TaskManager()
        worker_value = task_manager.workers._value
        logger.debug("remaining workers {}".format(worker_value))
        ((execution_id, send_queue, recv_queue), result) = task_manager.new_task(
            function_executor.execute_worker, func_name
        )
        if not result:
            raise HTTPException(status_code=500, detail="queue is full")
        logger.debug("new task succeed")
        if send_queue is None or recv_queue is None:
            raise HTTPException(status_code=500, detail="not a valid queue")
        if execution_id is None:
            raise HTTPException(status_code=500, detail="queue execution_id not valid")
        # transmit request to child process
        try:
            send_queue.put(req)
            send_queue.join()
        except Exception as e:
            logger.error("broken queue ", exception=str(e))
            raise HTTPException(500, detail="broken queue {}".format(str(e)))

        # poll and sleep, allow other requests
        while True:
            try:
                response = recv_queue.get(block=False, timeout=1)
                recv_queue.task_done()
                break
            except Exception:
                await asyncio.sleep(0.1)

        logger.debug("receive response")
        res_json = json.loads(response)
        res_json["execution_id"] = execution_id
        if res_json.get("result") == "finish":
            task_manager.release_queues(execution_id)
            logger.info("finish execution in create", execution_id=execution_id, req=str(req))
            return res_json
        logger.info("start execution", execution_id=execution_id, req=str(req), worker=worker_value)
        return res_json
    except HTTPException as e:
        logger.error("http exception occurred", exception=str(e))
        raise e
    except Exception as e:
        logger.error("http exception occurred", exception=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/table-functions/execs/{execution_id}")
async def receive_req(req: RequestObj, execution_id: str):
    try:
        # acquire send queue and recv queue resource by execution_id
        task_manager = TaskManager()
        worker_value = task_manager.workers._value
        logger.info("start execution:", execution_id=execution_id, worker_value=worker_value, req=req)

        if execution_id is None:
            raise HTTPException(status_code=400, detail="no execution_id provided")

        (send_queue, recv_queue) = task_manager.get_queues(execution_id)
        if send_queue is None or recv_queue is None:
            raise HTTPException(status_code=500, detail="queue map execution_id not valid")

        # transmit request to worker process
        try:
            send_queue.put(req)
            send_queue.join()
        except Exception as e:
            logger.error("broken queue ", exception=str(e))
            raise HTTPException(500, detail="broken queue {}".format(str(e)))
        logger.debug("send data")

        while True:
            try:
                response = recv_queue.get(block=False, timeout=1)
                recv_queue.task_done()
                break
            except Exception:
                await asyncio.sleep(0.1)

        res_json = json.loads(response)
        res_json["execution_id"] = execution_id
        if res_json["result"] == "finish":
            task_manager.release_queues(execution_id)
            logger.info(
                "finish execution",
                worker=task_manager.workers._value,
                execution_id=execution_id,
                req=str(req),
            )
        return res_json
    except HTTPException as e:
        logger.error("http exception occurred", exception=str(e))
        raise e
    except Exception as e:
        logger.error("http exception occurred", exception=str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/workers/pool-size")
async def repopulate(num_procs: int):
    pool_instance = TaskManager()
    if pool_instance.change_pool_size(num_procs):
        return "succeed"
    else:
        raise HTTPException(status_code=500, detail="repopulate internal error")


@app.get("/status")
async def heartbeat():
    return "success"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9720, log_config=get_logger_config())
