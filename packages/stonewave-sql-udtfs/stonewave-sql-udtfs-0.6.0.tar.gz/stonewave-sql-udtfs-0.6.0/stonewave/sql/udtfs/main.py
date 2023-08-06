import json
import os
import argparse
import sys
import pkgutil
import toml
import shutil
import time
import subprocess
import tarfile
from stonewave.sql.udtfs.function_executor import execute
from stonewave.sql.udtfs.constants import (
    USER_DEFINED_TABLE_FUNCTIONS_PATH,
    USER_DEFINED_TABLE_FUNCTION_INFO_FILE,
    SIGNATURE_LIST,
)
from stonewave.sql.udtfs.logger import logger
import stonewave.sql.udtfs.functions as built_in_funcs
from wheel_filename import parse_wheel_filename, InvalidFilenameError
from stonewave.sql.udtfs.test_utility import check_expected_parameters_list
from stonewave.sql.udtfs.load_function import load_function_by_name
from stonewave.sql.udtfs.version import sql_udtfs_version


def _list_udtfs_from_path(path, udtfs_list):
    try:
        for importer, modname, _ in pkgutil.iter_modules(path):
            info_path = os.path.join(importer.path, modname, USER_DEFINED_TABLE_FUNCTION_INFO_FILE)
            if not os.path.exists(info_path):
                logger.error("can not load function information", function_name=modname, info_path=info_path)
                continue
            info_toml = toml.load(info_path)
            udtfs_list[modname] = info_toml[SIGNATURE_LIST]
    except Exception as e:
        logger.error("load udtfs error", path=path, error=str(e))


def list_udtfs():
    if not os.path.exists(USER_DEFINED_TABLE_FUNCTIONS_PATH):
        os.mkdir(USER_DEFINED_TABLE_FUNCTIONS_PATH)
    udtfs_list = {}
    _list_udtfs_from_path(built_in_funcs.__path__, udtfs_list)
    _list_udtfs_from_path([USER_DEFINED_TABLE_FUNCTIONS_PATH], udtfs_list)
    return udtfs_list


def list_udtfs_cmd(args):
    udtfs_list = list_udtfs()
    if args.output_path:
        with open(args.output_path, "w") as f:
            f.write(json.dumps(udtfs_list, indent=4))
    else:
        print(json.dumps(udtfs_list, indent=4))


def _validate_function(func_path, func_name):
    sys.path.append(func_path)
    func = load_function_by_name(func_name)
    if func is None:
        shutil.rmtree(func_path)
        raise Exception("Can not find method implements from BaseFunction in stonewave.sql.udtfs.base_function")
    func_dir = func().__dir__()
    if "get_name" not in func_dir or "process" not in func_dir:
        raise Exception("Invalid function class, please implement get_name(self) and process(self, )")
    os.system("rm -rf /tmp/{}/**/__pycache__".format(func_name))


def _read_signature_list(path):
    info_toml = toml.load(path)
    return info_toml[SIGNATURE_LIST]


def _raise_register_exception(temporary_working_dir, msg):
    shutil.rmtree(temporary_working_dir)
    raise Exception(msg)


def register_udtf(func_name, func_path, update=False):
    if os.path.exists(os.path.join(os.path.dirname(__file__), "functions", func_name)):
        raise Exception("Should not update build-in table function: {}".format(func_name))

    if not os.path.exists(func_path):
        raise Exception("Failed to install python package: '{}' does not exist.".format(func_path))

    if os.path.splitext(func_path)[1] != ".gz":
        raise Exception(
            "Failed to install python package: please use eggfarm to help develop new python table function"
        )

    temporary_working_dir = "/tmp/{}_{}".format(func_name, int(round(time.time() * 1000)))

    # decompress tar file to temporary working dir
    # os.mkdir(temporary_working_dir)
    func_tar_file = tarfile.open(func_path)
    func_tar_file.extractall(path=temporary_working_dir)
    func_tar_file.close()

    # install python table function
    func_path = os.path.join(temporary_working_dir, func_name, func_name)
    commands = [
        "pip",
        "install",
        "--no-index",
        "-f",
        os.path.join(temporary_working_dir, func_name),
        func_name,
        "-t",
        func_path,
    ]
    installation = subprocess.run(
        commands,
        stderr=subprocess.PIPE,
    )

    if installation.returncode != 0:
        raise Exception("Failed to install python package: {}".format(installation.stderr.decode("utf-8")))

    try:
        filelist = os.listdir(os.path.join(func_path, func_name))
        for file in filelist:
            src = os.path.join(func_path, func_name, file)
            dst = os.path.join(func_path, file)
            shutil.move(src, dst)
        shutil.rmtree(os.path.join(func_path, func_name))
    except Exception as e:
        logger.error("project path name is not as same as package name", error_message=str(e))
        _raise_register_exception("Please make sure project path name is as same as package name")
    if not update:
        if os.path.exists(os.path.join(USER_DEFINED_TABLE_FUNCTIONS_PATH, func_name)):
            _raise_register_exception(temporary_working_dir, "Function already exists")
        info_path = os.path.join(func_path, USER_DEFINED_TABLE_FUNCTION_INFO_FILE)
        if not os.path.exists(info_path):
            logger.error(
                "can not load function information",
                function_name=func_name,
                info_path=USER_DEFINED_TABLE_FUNCTION_INFO_FILE,
            )
            _raise_register_exception(temporary_working_dir, "Please include info.toml for function information")
        try:
            check_expected_parameters_list(_read_signature_list(info_path))
        except Exception as e:
            _raise_register_exception(temporary_working_dir, str(e))
    else:
        existing_info_path = os.path.join(
            USER_DEFINED_TABLE_FUNCTIONS_PATH, func_name, USER_DEFINED_TABLE_FUNCTION_INFO_FILE
        )
        if not os.path.exists(existing_info_path):
            _raise_register_exception(
                temporary_working_dir, "User defined table function does not exists: {}".format(func_name)
            )
        existing_signature_list = _read_signature_list(existing_info_path)
        new_info_path = os.path.join(func_path, USER_DEFINED_TABLE_FUNCTION_INFO_FILE)
        if not os.path.exists(new_info_path):
            logger.error(
                "can not load function information",
                function_name=func_name,
                info_path=USER_DEFINED_TABLE_FUNCTION_INFO_FILE,
            )
            _raise_register_exception(temporary_working_dir, "Please include info.toml for function information")
        new_signature_list = _read_signature_list(new_info_path)
        if existing_signature_list != new_signature_list:
            _raise_register_exception(temporary_working_dir, "Should not update table function signature list")
    _validate_function(os.path.join(temporary_working_dir, func_name), func_name)

    shutil.copytree(func_path, os.path.join(USER_DEFINED_TABLE_FUNCTIONS_PATH, func_name), dirs_exist_ok=True)
    shutil.rmtree(temporary_working_dir)


def register_udtf_cmd(args):
    func_name = args.function_name
    func_path = args.function_path
    update = args.update
    try:
        register_udtf(func_name, func_path, update)
    except Exception as e:
        print(str(e))
        exit(-1)


def exec_udtf_cmd(args):
    execute(args.function_name, input, sys.stdout)


def remove_udtf(function_name):
    os.system("rm -rf {}/{}".format(USER_DEFINED_TABLE_FUNCTIONS_PATH, function_name))


def remove_udtf_cmd(args):
    remove_udtf(args.function_name)


def execute_command():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="""
        Command sw_py_udtf
        Usage Examples:

        1) exec
        $ sw_py_udtf exec --function-name <name>
        Execute function, please integrate to stonewave service. Function name is required.
        2) list 
        $ sw_py_udtf list --output-path <path>
        List all accessiable python table functions. Output path is not required. If no
        output path, with list all table functions to stdout.
        3) register
        $ sw_py_udtf register --function-name <name> --function-path <path>
        Function name and function path are required. currently only support file system path
        for user defined table function python wheel package
        4) remove
        $ sw_py_udtf exec --function-name remove
        Remove table function. Function name is required
        """,
    )
    parser.add_argument("-V", "--version", action="version", version=sql_udtfs_version())
    subparsers = parser.add_subparsers()

    exec_subparser = subparsers.add_parser("exec")
    exec_subparser.add_argument(
        "-n",
        "--function-name",
        required=True,
        type=str,
        help="user defined table function name",
    )
    exec_subparser.set_defaults(callback=exec_udtf_cmd)

    list_subparser = subparsers.add_parser("list")
    list_subparser.add_argument(
        "-o",
        "--output-path",
        default="",
        type=str,
        help="output udtfs list to specific path",
    )
    list_subparser.set_defaults(callback=list_udtfs_cmd)

    register_subparser = subparsers.add_parser("register")
    register_subparser.add_argument(
        "-n",
        "--function-name",
        required=True,
        type=str,
        help="user defined table function name",
    )
    register_subparser.add_argument(
        "-p",
        "--function-path",
        required=True,
        type=str,
        help="user defined table function package path",
    )
    register_subparser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="flag to update existing user defined table function",
    )
    register_subparser.set_defaults(callback=register_udtf_cmd)

    remove_subparser = subparsers.add_parser("remove")
    remove_subparser.add_argument(
        "-n",
        "--function-name",
        required=True,
        type=str,
        help="user defined table function name",
    )
    remove_subparser.set_defaults(callback=remove_udtf_cmd)

    args = parser.parse_args()
    args.callback(args)


if __name__ == "__main__":
    execute_command()
