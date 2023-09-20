from nodes import Parameter


def identity(x):
    return x


def with_parameters(object_data: dict):
    parameters = object_data.get("parameters", [])
    mapped_parameters = list(map(lambda parameter: Parameter(**parameter), parameters))

    return {**object_data, 'parameters': mapped_parameters}


def with_parameter(object_data: dict):
    parameter = object_data["name"]
    mapped_parameter = Parameter(**parameter)

    return {**object_data, 'name': mapped_parameter}
