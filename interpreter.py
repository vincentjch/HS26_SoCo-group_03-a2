import json
import pprint
import sys

import helpers

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
    assert second!=0, "Cannot divide by zero"
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
    assert second>0, "Cannot mod by zero"
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
# looks like: ["new_array", "int", 6], but names come from "set": names "squares" and "new_array", then "int" and 6, so 2 args instead of 3
def do_new_array(envs, args):
    assert len(args)==2 # type and length of array
    assert isinstance(args[0], str)
    
    # do() passes everything after name of the operation, so data_type=args[0] ...

    data_type=args[1]
    assert args[0] in TYPES #note: the type entries are strings "int", not the direct type int. Hence in TYPES and not TYPES.values()
        
    length=do(envs, args[1])
    assert isinstance(length, int) and length>=0 # 0 also allowed, for example with for loop
    
    if data_type=="float": # compare with float string, not actual float type
        array=[0.0]*length
    else:
        array=[0]*length    #any other type
    # env set already done by do_set() here
    #env_set(envs, name, array)
    return array


#looks like: ["array_get", ["get", "m"], 0]
#looks like: ["array_get", ["get", "m"], 0]
def do_array_get(envs, args):
    assert len(args)==2 #array and index
    array=do(envs, args[0]) #evaluate the array, for example ["get", "m"]
    assert isinstance(array, list), "array_get needs an array"
    index=do(envs, args[1])
    assert isinstance(index, int), "Index has to be an int"
    assert 0<=index<len(array), "Index out of bounds: " + str(index) #negative indexes are not allowed either
    return array[index]


#looks like: ["array_set", ["get", "squares"], ["get", "i"], ["mult", ["get", "i"], ["get", "i"]]]
def do_array_set(envs, args):
    assert len(args)==3 #array, index and new value
    array=do(envs, args[0]) #evaluate the array, for example ["get", "squares"]
    assert isinstance(array, list), "array_set needs an array"
    index=do(envs, args[1])
    assert isinstance(index, int), "Index has to be an int"
    assert 0<=index<len(array), "Index out of bounds: " + str(index)
    value=do(envs, args[2]) #evaluate the new value
    array[index]=value #changes the array itself, so "squares" in the environment changes too
    return value


def do_array_size(envs, args):
    pass


########DECLARED TYPES##########
#looks like: ["struct", "Point", [["x", "int"], ["y", "int"]]]
def do_struct(envs, args):
    assert len(args)==2

    type_name=args[0]
    fields=args[1]
    
    assert isinstance(type_name, str)
    assert isinstance(fields, list)
    for entry in fields:
        assert isinstance(entry, list)
        assert isinstance(entry[0], str)    #first entry is the name
        assert entry[1] in TYPES     #second entry is of known type
        assert type_name not in TYPES, "Type name already defined" #make sure the type dosn't exists yet
    
    TYPES[type_name]=fields #now becomes a knew object type
    return None


#looks like: ["make", "Point", 7, 8]
def do_make(envs, args):
    assert len(args)>=1
    type_name=args[0]
    assert type_name in TYPES, "Unknown type"
    fields=TYPES[type_name] #get the fields tied to the specific type we want to build. fields looks something like [["x", "int"], ["y", "int"]]
    values = [do(envs, a) for a in args[1:]] #evaluate the other entries

    assert len(fields)==len(values) #we check there are the same number of fields as values

    field_values={}     #we will store the fieds and corresponding values here, after ziping them together and checks
    for field, value in zip(fields, values):
        field_name=field[0]     #because field looks like ["x", "int"]
        field_type=field[1]
        assert isinstance(value, TYPES[field_type]), "Incompatible types. Expected:" + field_type + "provided was: " + type(value) #check the value is of correct type

        field_values[field_name]=value

    instance={
        "type": type_name,
        "fields": field_values
    }
    return instance


#looks like: ["field_get", "p", "x"]]
def do_field_get(envs, args):
    assert len(args)==2 #instance of a struct and name of one of its fields

    #we distinguish two cases here: 
    #do we have     ["field_get", ["get", "p"], "x"]
    #or             ["field_get", "p", "x"]
    if isinstance(args[0], list):
        instance=do(envs, args[0])
    else: 
        instance=env_get(envs, args[0])

    #check that the instance arg is a struct
    assert isinstance(instance, dict)
    assert "type" in instance and "fields" in instance
    assert instance["type"] in TYPES 
    assert isinstance(instance["fields"], dict)


    field_name=args[1]
    #remember: instance is a dict of dicts, like: {"type": "Point", "fields": {"x": 7, "y": 8}}
    instance_fields=instance["fields"]
    assert field_name in instance_fields #we make sure field_name appears in instanc_fields
    return instance_fields[field_name]


#looks like: ["field_set", "p", "x", 10]
def do_field_set(envs, args):
    assert len(args)==3
    #re-use the structure of do_field_get
    if isinstance(args[0], list):
        instance=do(envs, args[0])
    else: 
        instance=env_get(envs, args[0])

    assert isinstance(instance, dict)
    assert "type" in instance and "fields" in instance
    assert instance["type"] in TYPES 
    assert isinstance(instance["fields"], dict)

    concerned_field=do(envs, args[1]) #which field to replace/set?
    new_value=do(envs, args[2]) #evaluate the value to set

    #we now need to check that new_value is of the same type as the field we want to replace/define it
    #retrieve the type:
    type_name=instance["type"]
    fields=TYPES[type_name]
    #find the concerned field
    for name, declared_type in fields:
        if name ==concerned_field:
            #check that the types correspond
            assert TYPES[declared_type]==type(new_value), "Cannot set, expected type" + declared_type
            #note: without the TYPES[], we were comparing int with "int" etc
            break

    #only then, replace/set:
    instance["fields"][concerned_field]=new_value


#looks like: ["range", 6], gives the array [0, 1, 2, 3, 4, 5]
def do_range(envs, args):
    assert len(args)==1
    n=do(envs, args[0])
    assert isinstance(n, int) and n>=0, "range needs a non negative int"
    return list(range(n))


#looks like: ["for", "i", ["range", 6], body] (very similar to python: for i in range(6))
def do_for(envs, args):
    assert len(args)==3 #loop variable name, array, body
    var_name=args[0]
    assert isinstance(var_name, str)

    array=do(envs, args[1]) #evaluate the array, for example ["range", 6] or ["get", "squares"]
    assert isinstance(array, list), "for can only loop over arrays"
    body=args[2] #not evaluated here, it gets evaluated in every iteration

    result=None #empty array: the loop evaluates to null
    for element in array:
        #bind the loop variable in a local environment, same idea as the parameters in do_call
        envs.append({var_name: element})
        result=do(envs, body)
        envs.pop()
    return result


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


#create a function
def do_func(envs, args):
    assert len(args) == 3
    params = args[0]
    return_type=args[1]
    #will need to check that return_type is in int, float, array or struct once struct is coded
    body = args[2]
    return ["func", params, return_type, body]


#looks like: ["if", ["lt", 2, 3], 111, 222] so (if, condition, then, else)
def do_if(envs, args):
    assert len(args)==3
    
    cond_expr=do(envs, args[0])
    
    if cond_expr:
        branch=args[1]
    else:
        branch=args[2]

    if branch==[]:
        return None

    result=do(envs, branch)
    return result


def do_null(envs, args):
    assert len(args)==0
    return None


#looks like: ["print", ["mult", 6, 7]]
def do_print(envs, args):
 
    # assert len(args)==1
    # assert isinstance(args[0], list)   would rejected valid programs like ["print", ...]
    assert len(args) >= 1 # one or MORE than one as well

    # evaluate each argument: args is the list AROUND the arguments, so do(envs, args) crashed
    values = [do(envs, arg) for arg in args]
    for value in values:
        pprint.pprint(value)
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
                        
            #assert isinstance(values[index], TYPES[param_type]), func_name + "expect a" + param_type + " and got " + str(values[index])

            # instead check at every function call that every argument passes
            # the assigned type of the param. Error than outputs func, param and value
            assert helpers.is_of_type(values[index], param_type, TYPES), func_name + ": parameter " + param_name + " expects " + param_type + ", got " + str(values[index])

        else:   #if not, proceed as before
            param_name=param
        local_env[param_name] = values[index]

    envs.append(local_env)
    result = do(envs, body)
    envs.pop()
    return result


def do(envs, expr):
    #modified so it doesn't just accept ints as atoms but also arrays and other defined types
    if not isinstance(expr, list):
        return expr
    
    assert isinstance(expr, list)
    func_name = expr[0]
    
    args = expr[1:]

    assert func_name in OPS, "Operation without do in name: " + str(func_name)

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

##########################

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
