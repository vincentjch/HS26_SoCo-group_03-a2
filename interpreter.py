import json
import pprint
import sys

#######ARITHMETIC########
def do_add(envs, args):
    assert len(args) == 2
    first = do(envs, args[0])
    second = do(envs, args[1])
    return first + second

def do_sub(envs, args):
    assert len(args) == 2
    first = do(envs, args[0])
    second = do(envs, args[1])
    return first - second

def do_abs(envs, args):
    assert len(args) == 1
    value = do(envs, args[0])
    if value >= 0:
        return value
    if value < 0:
        return -value

def do_mult(envs, args):
    assert len(args)==2
    first=do(envs, args[0])
    second=do(envs, args[1])
    return first*second

def do_div(envs, args):
    assert len(args)==2
    first=do(envs, args[0])
    second=do(envs, args[1])
    assert second!=0
    return first/second

def do_pow(envs, args):
    assert len(args)==2
    first=do(envs, args[0])
    second=do(envs, args[1])
    return first**second

def do_mod(envs, args):
    assert len(args)==2
    first=do(envs, args[0])
    second=do(envs, args[1])
    return first%second


#######COMPARISONS##########
def do_lt(envs, args):
    assert len(args)==2
    first=do(envs, args[0])
    second=do(envs, args[1])
    assert isinstance(first, (int, float)), "Invalid type"
    assert isinstance(second, (int, float)), "Invalid type"
    return first < second

def do_gt(envs, args):
    assert len(args)==2
    first=do(envs, args[0])
    second=do(envs, args[1])
    assert isinstance(first, (int, float)), "Invalid type"
    assert isinstance(second, (int, float)), "Invalid type"
    return first > second

def do_le(envs, args):
    assert len(args)==2
    first=do(envs, args[0])
    second=do(envs, args[1])
    assert isinstance(first, (int, float)), "Invalid type"
    assert isinstance(second, (int, float)), "Invalid type"
    return first <= second

def do_ge(envs, args):
    assert len(args)==2
    first=do(envs, args[0])
    second=do(envs, args[1])
    assert isinstance(first, (int, float)), "Invalid type"
    assert isinstance(second, (int, float)), "Invalid type"
    return first >= second

def do_equal(envs, args):
    assert len(args)==2
    first=do(envs, args[0])
    second=do(envs, args[1])
    assert isinstance(first, (int, float)), "Invalid type"
    assert isinstance(second, (int, float)), "Invalid type"
    return first = second

def do_not_equal(envs, args):
    assert len(args)==2
    first=do(envs, args[0])
    second=do(envs, args[1])
    assert isinstance(first, (int, float)), "Invalid type"
    assert isinstance(second, (int, float)), "Invalid type"
    return first != second


########FUNCTIONALITIES##########
def do_set(envs, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    name = args[0]
    value = do(envs, args[1])
    env_set(envs, name, value)
    return value


def env_set(envs, name, value):
    assert isinstance(name, str)
    envs[-1][name] = value


def do_get(envs, args):
    assert len(args) == 1
    assert isinstance(args[0], str)
    name = args[0]
    return env_get(envs, name)


def do_seq(envs, args):
    assert len(args) > 0
    for item in args:
        result = do(envs, item)
    return result


def do_func(envs, args):
    assert len(args) == 2
    params = args[0]
    body = args[1]
    return ["func", params, body]


def env_get(envs, name):
    assert isinstance(name, str)
    for env in reversed(envs):
        if name in env:
            return env[name]
    assert False, "Unknown name: " + name


def do_call(envs, args):
    assert len(args) >= 1

    func_name = args[0]
    values = [do(envs, a) for a in args[1:]]

    fun = env_get(envs, func_name)

    assert isinstance(fun, list) and (len(fun) == 3) and (fun[0] == "func")
    params = fun[1]
    body = fun[2]

    assert len(params) == len(values)

    local_env = dict()
    for index, param_name in enumerate(params):
        local_env[param_name] = values[index]
    envs.append(local_env)
    result = do(envs, body)
    envs.pop()
    return result


def do(envs, expr):
    if isinstance(expr, int):
        return expr

    assert isinstance(expr, list)
    func_name = expr[0]
    args = expr[1:]
    assert func_name in OPS, (
        "only add, abs, sub, set, get, seq, func, and call are supported in our DSL. "
        + func_name
        + " is not supported"
    )
    fun = OPS[func_name]
    return fun(envs, args)


def get_ops():
    ops = dict()
    for name, fun in globals().items():
        if name.startswith("do_"):
            ops[name.replace("do_", "")] = fun
    return ops


OPS = get_ops()


def main():
    assert len(sys.argv) == 2, "Usage: interpreter.py <filename>"
    filename = sys.argv[1]
    with open(filename, "r") as f:
        program = json.load(f)
        envs = [dict()]
        print("Environment before: ")
        print(envs)
        result = do(envs, program)
        print("Result: ")
        print(result)
        print("Environment after: ")
        print(envs)


if __name__ == "__main__":
    main()
