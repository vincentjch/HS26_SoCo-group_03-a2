# Return True if the value has the given type, otherwise False
# built in types are "int", "float" and "array"
# a struct value is a dict like {"type": "Point", "fields": {"x": 7, "y": 8}}
def is_of_type(value, type_name, types):
    if type_name == "int" or type_name == "float" or type_name == "array":
        return isinstance(value, types[type_name])
    if isinstance(value, dict) and "type" in value:
        return value["type"] == type_name
    return False

def main():

    # examples here
    types = {"int": int, "float": float, "array": list, "Point": [["x", "int"], ["y", "int"]]}
    points = {"type": "Point", "fields": {"x": 7, "y": 8}}

    print(is_of_type(5, "int", types))          # true
    print(is_of_type(5, "float", types))        # False because here no automatic casting from int to float
    print(is_of_type(points, "Point", types))   # true

if __name__ == "__main__":
    main()