import functools
import contextlib
import sys
import math
import datetime

# def _import(name, globals=None, locals=None, fromlist=None, level=-1):
#     if globals is None:
#         globals = {}
#     if locals is None:
#         locals = {}
#     if fromlist is None:
#         fromlist = []
#     if name in _ALLOWED_MODULES:
#         return __import__(name, globals, locals, level)
#     raise ImportError(name)

def _import(name, globals=None, locals=None, fromlist=None, level=-1):
    raise Exception("Import is prohibited inside templates")

BUILTINS = {
    "__import__": _import,
    "all": all,
    "any": any,
    "ascii": ascii,
    "bin": bin,
    "bool": bool,
    "bytearray": bytearray,
    "bytes": bytes,
    "callable": callable,
    "chr": chr,
    "complex": complex,
    "datetime": datetime,
    "dict": dict,
    "dir": dir,
    "divmod": divmod,
    "enumerate": enumerate,
    "False": False,
    "filter": filter,
    "float": float,
    "format": format,
    "frozenset": frozenset,
    "getattr": getattr,
    "hasattr": hasattr,
    "hash": hash,
    "hex": hex,
    "int": int,
    "isinstance": isinstance,
    "issubclass": issubclass,
    "iter": iter,
    "len": len,
    "list": list,
    "map": map,
    "math": math,
    "max": max,
    "min": min,
    "next": next,
    "None": None,
    "oct": oct,
    "ord": ord,
    "pow": pow,
    "range": range,
    "reduce": functools.reduce,
    "repr": repr,
    "reversed": reversed,
    "round": round,
    "set": set,
    "setattr": setattr,
    "slice": slice,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "True": True,
    "tuple": tuple,
    "type": type,
    "zip": zip,
}

# In case we need to filter
# Globals must contain __builtins__ entry 
def exec_code(code, globals=None, locals=None):
    if globals is None:
        globals = {"__builtins__": BUILTINS}
    if locals is None:
        locals = {}
    exec(code, globals, locals)
    return globals, locals

def eval_code(code, globals=None, locals=None):
    if globals is None:
        globals = {"__builtins__": BUILTINS}
    if locals is None:
        locals = {}
    return eval(code, globals, locals)

# TODO: Not working
# @contextlib.contextmanager
# def safe_code():
#     modules = sys.modules
#     builtins = globals()["__builtins__"]
#     sys.modules = []
#     globals()["__builtins__"] = BUILTINS
#     sys.modules = []
#     try:
#         yield
#     finally:
#         print("restauring data")
#         globals()["__builtins__"] = builtins
#         sys.modules = modules


# with safe_code():
#     print("print" in dir(globals()["__builtins__"]))


def interp(f, **kw):
    return eval_code("f{}".format(repr(f)), None, kw)


TEMP_VAR_NAME = "rewqrewvnkjvnkrntlwkqerjweholifuhlnrkjnqlrekwjcvhdlsiurenqwlfkjnfdasfsd"

def eval_as(parameters, value, variables=None, globals=None):
    """
        Usage: 
    """
    if variables is None:
        variables = {}
    if isinstance(parameters, (list, tuple)):
        parameters = ", ".join(parameters)

    # Eval the values
    values_code = "({})".format(value)
    value = eval_code(values_code, globals, locals=variables)

    # Assign the values
    assign_statment = "({}) = {}".format(
        parameters,
        TEMP_VAR_NAME
    )
    res = {TEMP_VAR_NAME: value}
    exec_code(assign_statment, globals=globals, locals=res)
    res.pop(TEMP_VAR_NAME)
    return res

def iter_as(parameters, value, variables=None, globals=None):
    """
        Parameters:
        - parameters: parameters of the loop
        - value: the value on which we iter
        - variables=None: extra variables which will be used to evaluate "value"
        - globals: globals values to use (by default, used the safe ones of this module)
        Usage: list(iter_as("a, b", "(i, i + 5) for i in range(10)"))
    """
    if variables is None:
        variables = {}
    if isinstance(parameters, (list, tuple)):
        parameters = ", ".join(parameters)
    # Prepare assignement statement
    # We use an improbable variable name to avoid colision
    parameters = "({}) = {}".format(
        parameters,
        TEMP_VAR_NAME
    )
    value = "({})".format(value)  # protect expression, e.g. "i for i in range(5)" would end up in error
    values = eval_code(value, globals, locals=variables)
    for it in values:
        loop_vars = {TEMP_VAR_NAME: it}
        exec_code(parameters, globals=globals, locals=loop_vars)
        loop_vars.pop(TEMP_VAR_NAME)
        yield loop_vars

# list(iter_as("a, b", "(i, i + 5) for i in range(10)"))