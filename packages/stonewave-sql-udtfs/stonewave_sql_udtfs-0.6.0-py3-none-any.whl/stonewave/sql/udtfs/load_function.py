import importlib
import inspect
from stonewave.sql.udtfs.base_function import BaseFunction
from stonewave.sql.udtfs.logger import logger


def _find_base_function_from_lib(lib):
    for mod in dir(lib):
        method = eval("lib." + mod)
        if inspect.isclass(method):
            if issubclass(method, BaseFunction):
                if not issubclass(BaseFunction, method):
                    return method
    return None


def load_function_by_name(name):
    try:
        # built-in table functions
        lib = importlib.import_module("stonewave.sql.udtfs.functions.{}".format(name))
        logger.info("load built-in table function", function_name=name)
        return _find_base_function_from_lib(lib)
    except:
        try:
            # user defined table functions
            # functions path has been append to sys.path when starting the executor

            lib = importlib.import_module(name)
            logger.info("load user defined table function", function_name=name)
            return _find_base_function_from_lib(lib)
        except:
            try:
                importlib.invalidate_caches()
                lib = importlib.import_module(name)
                logger.info("clean cache and load user defined table function", function_name=name)
                return _find_base_function_from_lib(lib)
            except Exception as e:
                logger.error("function not found", function_name=name, error=str(e))
                return None
