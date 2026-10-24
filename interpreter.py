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
    return first == second

def do_not_equal(envs, args):
    assert len(args)==2
    first=do(envs, args[0])
    second=do(envs, args[1])
    assert isinstance(first, (int, float)), "Invalid type"
    assert isinstance(second, (int, float)), "Invalid type"
    return first != second

########ARRAYS########
def do_new_array(envs, args):
    assert len(args)==3 #name, type and length of the array
    assert isinstance(args[0], str)
    
    name=envs, args[0] #no need of do(), its already a string
    #check if do() needed after coding datatypes
    data_type=args[1]
    size=do(envs, args[2])
    assert isinstance(size, int) and size>=0
    if data_type==float:
        array=[0.0]*size
    else:
        array=[0]*size
    env_set(envs, name, array)
    return array

def do_array_get(envs, args):
    pass

def do_array_set(envs, args):
    pass

def do_array_size(envs, args):
    pass

########DECLARED TYPES##########
def do_struct(envs, args):
    assert len(args)==2

    type_name=args[0]
    structure=args[1]
    
    assert isinstance(type_name, str)
    assert isinstance(structure, list)
    for entry in structure:
        assert isinstance(entry, list)
        assert isinstance(entry[0], str)    #first entry is the name
        #assert isinstance(entry[1],  ) will check here if the second entry is of any known type or new declared struct type




def do_make(envs, args):
    assert len(args)>=1


def do_field_get(envs, args):
    pass

def do_field_set(envs, args):
    pass

########FUNCTIONALITIES##########
#create or update a variable
def do_set(envs, args):
    assert len(args) == 2
    assert isinstance(args[0], str)
    name = args[0]
    value = do(envs, args[1])
    #store it in the environment
    env_set(envs, name, value)
    return value

#store a name, value in the environment
def env_set(envs, name, value):
    assert isinstance(name, str)
    envs[-1][name] = value

#get a variable from our environment, using env_get
def do_get(envs, args):
    assert len(args) == 1
    assert isinstance(args[0], str)
    name = args[0]
    return env_get(envs, name)

#allows interpreter to do stuff iteritavely (treats args one after the other)
def do_seq(envs, args):
    assert len(args) > 0
    for item in args:
        result = do(envs, item)
    return result


def do_func(envs, args):
    assert len(args) == 3
    params = args[0]
    return_type=args[1]
    #will need to check that return_type is in int, float, array or struct once struct is coded
    body = args[2]
    return ["func", params, return_type, body]

def do_if(envs, args):
    assert len(args)==3
    cond_expr=do(envs, args[0])
    #previous line could crash without my addition to do()
    if cond_expr==[]:
        return None
    if cond_expr:
        then_expr=do(envs, args[1])
        if then_expr==[]:
            return None
        return then_expr
    else_expr=do(envs, args[2])
    if else_expr==[]:
        return None
    return else_expr

def do_null(envs, args):
    assert len(args)==0
    return None

def do_print(envs, args):
    values=[]
    for thing in args:
        values.append(do(envs, thing))
    pprint.pprint(values)
    return None

def env_get(envs, name):
    assert isinstance(name, str)
    for env in reversed(envs):
        if name in env:
            return env[name]
    assert False, "Unknown name: " + name


def do_call(envs, args):
    func_name = args[0]

    assert len(args) >= 1 or func_name=="null"

    values = [do(envs, a) for a in args[1:]]
    
    #fun is a list representing a function
    #looked up in the environmnet
    fun = env_get(envs, func_name)

    assert isinstance(fun, list) and (len(fun) == 4) and (fun[0] == "func") #len is 4 because of return type
    params = fun[1]
    return_type=fun[2]
    body = fun[3]
    assert len(params) == len(values)

    local_env = dict()
    for index, param in enumerate(params): #enumerating allows us to know which value belongs to which parameter
        #we need an extra check here
        if isinstance(param, list): #if list: then type is specified
            param_name=param[0]
            param_type=param[1]
            #check, at every function call, that each argument satisfies the
            #annotated type of the parameter
            assert isinstance(values[index], TYPES[param_type]), func_name + "expect a" + param_type + " and got " + str(values[index])
        else:   #if not, proceed as before
            param_name=param
        local_env[param_name] = values[index]

    envs.append(local_env)
    result = do(envs, body)
    envs.pop()
    return result


def do(envs, expr):
    if isinstance(expr, int):
        return expr

    #my do_if block was crashing, added this to handle the [] seperately
    if expr==[]:
        return []
    
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

#######DEFINED VARIABLE TYPES######
TYPES={"int": int, "float":float, "array":list} #will possibly be completed with new, user declared types

#######OPERATIONS######
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
