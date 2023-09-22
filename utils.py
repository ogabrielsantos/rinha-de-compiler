from nodes import (
    Binary,
    BinaryOp,
    Bool,
    Call,
    First,
    Function,
    If,
    Int,
    Let,
    Parameter,
    Print,
    Second,
    Str,
    Tuple,
    Var,
)


def identity(x):
    return x


def with_parameters(object_data: dict):
    parameters = object_data.get("parameters", [])
    mapped_parameters = list(map(lambda parameter: Parameter(**parameter), parameters))

    return {**object_data, "parameters": mapped_parameters}


def with_parameter(object_data: dict):
    parameter = object_data["name"]
    mapped_parameter = Parameter(**parameter)

    return {**object_data, "name": mapped_parameter}


def with_binary_operation(object_data: dict):
    op = object_data["op"]
    mapped_op = BinaryOp(op)

    return {**object_data, "op": mapped_op}


SUPPORTED_NODES = {
    Var.kind: (Var, identity),
    Function.kind: (Function, with_parameters),
    Call.kind: (Call, identity),
    Let.kind: (Let, with_parameter),
    Str.kind: (Str, identity),
    Int.kind: (Int, identity),
    Bool.kind: (Bool, identity),
    If.kind: (If, identity),
    Binary.kind: (Binary, with_binary_operation),
    Tuple.kind: (Tuple, identity),
    First.kind: (First, identity),
    Second.kind: (Second, identity),
    Print.kind: (Print, identity),
}


def to_ast_node(object_data: dict):
    if kind := object_data.get("kind"):
        if node_handler := SUPPORTED_NODES.get(kind):
            node, handler = node_handler
            node_arguments = handler(object_data)

            return node(**node_arguments)

    return object_data
