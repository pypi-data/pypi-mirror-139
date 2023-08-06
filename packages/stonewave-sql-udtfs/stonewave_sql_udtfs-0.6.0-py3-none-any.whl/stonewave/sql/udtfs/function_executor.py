import sys
import os
import json
from stonewave.sql.udtfs.load_function import load_function_by_name
from stonewave.sql.udtfs.logger import logger
from stonewave.sql.udtfs.constants import USER_DEFINED_TABLE_FUNCTIONS_PATH
from stonewave.sql.udtfs.protocol.fsm.apply_function_fsm import ApplyFunctionFsm
from stonewave.sql.udtfs.protocol.fsm.eval_function_fsm import EvalFunctionFsm
from stonewave.sql.udtfs.protocol.fsm.eval_function_with_table_param_fsm import (
    EvalFunctionWithTableParamFsm,
)
from stonewave.sql.udtfs.protocol.fsm.result_batch_sender import (
    SharedMemoryRecordBatchSender,
)
from pydantic import BaseModel
from typing import Optional
from stonewave.sql.udtfs.protocol.shared_memory_record_batch_reader import (
    SharedMemoryRecordBatchReader,
)
import gc


class ResponseObj(BaseModel):
    pid: Optional[int] = None
    result: Optional[str] = None
    error: Optional[str] = None


def execute_child_worker(func_name, recv_queue, send_queue):
    def respond(result, error=None):
        res = json.dumps({"result": result, "error": error})
        logger.debug("send response", function=func_name, response=res)
        send_queue.put(res)
        send_queue.join()

    try:
        if not USER_DEFINED_TABLE_FUNCTIONS_PATH in sys.path:
            sys.path.append(USER_DEFINED_TABLE_FUNCTIONS_PATH)
        func_sys_path = os.path.join(USER_DEFINED_TABLE_FUNCTIONS_PATH, func_name)
        if not func_sys_path in sys.path:
            sys.path.append(func_sys_path)

        function = load_function_by_name(func_name)
        if function is None:
            command = recv_queue.get()
            recv_queue.task_done()
            respond(
                result="finish",
                error="function not found, name is {}".format(func_name),
            )
            return

        func = function()
        fsm = None
        batch_sender = SharedMemoryRecordBatchSender()

        while True:
            logger.debug("waiting for request", function=func_name)
            command = recv_queue.get()
            recv_queue.task_done()
            logger.debug("receive request", function=func_name, request=command)
            request = command
            method, params = request.method, request.params

            if fsm is None:
                if method == "apply":
                    fsm = ApplyFunctionFsm(func, batch_sender)
                elif method == "eval":
                    fsm = EvalFunctionFsm(func, batch_sender)
                elif method == "eval_with_table_param":
                    fsm = EvalFunctionWithTableParamFsm(func, batch_sender)
            fsm_trigger = getattr(fsm, method, None)
            if fsm_trigger:
                try:
                    fsm_trigger(params, respond)
                except Exception as e:
                    logger.error("error occurred during function execution", error=str(e))
                    params = None
                    request = None
                    fsm._clean_up()
                    respond(result="finish", error=e.args[0])
                    break
                logger.debug("finish executing request", function=func_name, state=fsm.state)
                if fsm.is_end():
                    logger.info("finish function execution", function=func_name)
                    break
            else:
                respond(result="finish", error="invalid_method=" + method)
                break
        if func_sys_path in sys.path:
            sys.path.remove(func_sys_path)
        if USER_DEFINED_TABLE_FUNCTIONS_PATH in sys.path:
            sys.path.remove(USER_DEFINED_TABLE_FUNCTIONS_PATH)
    except Exception as e:
        logger.error("error occured", error=str(e))
        respond("finish", error=str(e))
    finally:
        fsm = None
        batch_sender = None
        function = None
        fsm_trigger = None


def execute_worker(func_name, recv_queue, send_queue):
    execute_child_worker(func_name, recv_queue, send_queue)
    ## unlink shared memory objects to release memory
    gc.collect()
    SharedMemoryRecordBatchReader.shared_memory_objects = []


# this protocol roughly follows json-rpc protocol's request/response format
# stdin/stdout is used as transport (in_func/out_io)
# https://en.wikipedia.org/wiki/JSON-RPC
# a request contains three properties: method, params, id
# a response contains three properties: result, error, id
def execute(func_name, in_func, out_io):
    sys.path.append(USER_DEFINED_TABLE_FUNCTIONS_PATH)
    sys.path.append(os.path.join(USER_DEFINED_TABLE_FUNCTIONS_PATH, func_name))
    logger.info("start function execution", function=func_name)
    sys.path.append(os.path.join(USER_DEFINED_TABLE_FUNCTIONS_PATH, func_name))
    function = load_function_by_name(func_name)
    func = function()

    fsm = None
    batch_sender = SharedMemoryRecordBatchSender()

    while True:
        logger.debug("waiting for request", function=func_name)
        command = in_func()
        logger.debug("receive request", function=func_name, request=command)
        request = json.loads(command)
        method, params, request_id = request["method"], request["params"], request["id"]

        def respond(result, error=None):
            res = json.dumps({"result": result, "error": error, "id": request_id})
            logger.debug("send response", function=func_name, response=res)
            print(
                res,
                file=out_io,
                flush=True,
            )

        if fsm is None:
            if method == "apply":
                fsm = ApplyFunctionFsm(func, batch_sender)
            elif method == "eval":
                fsm = EvalFunctionFsm(func, batch_sender)
            elif method == "eval_with_table_param":
                fsm = EvalFunctionWithTableParamFsm(func, batch_sender)
        fsm_trigger = getattr(fsm, method, None)
        if fsm_trigger:
            try:
                fsm_trigger(params, respond)
            except Exception as e:
                logger.error("error occurred during function execution", error=str(e))
                respond(result=None, error=e.args[0])
                break
            logger.debug("finish executing request", function=func_name, state=fsm.state)
            if fsm.is_end():
                logger.info("finish function execution", function=func_name)
                break
        else:
            respond(result=None, error="invalid_method=" + method)


if __name__ == "__main__":
    func_name = sys.argv[1]
    execute(func_name, input, sys.stdout)
