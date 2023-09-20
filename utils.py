from nodes import Parameter, BinaryOp


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
