from enum import Enum
from functools import cache

import binary_operations


class Location:
    start: int
    end: int
    filename: str


class Var:
    kind: str = "Var"
    text: str
    location: Location

    def __init__(self, text: str, **kwargs):
        self.text = text

    def execute(self, **kwargs):
        return kwargs.get("namespace", {}).get(self.text)


class Parameter:
    text: str
    location: Location

    def __init__(self, text: str, **kwargs):
        self.text = text


class HashableDict(dict):
    def __hash__(self):
        return hash(frozenset(self))


class Function:
    kind: str = "Function"
    parameters: list[Parameter]
    value: "Term"
    location: Location

    def __init__(self, parameters: list[Parameter], value: "Term", **kwargs):
        self.parameters = parameters
        self.value = value

    def execute(self, **kwargs):
        global_namespace = kwargs.get("namespace", {})
        parameters = list(map(lambda parameter: parameter.text, self.parameters))
        total_parameters = len(parameters)

        @cache  # @todo yep, it's a dumb and risky optimization
        def function(*function_args, **function_kwargs):
            total_arguments = len(function_args)

            if total_arguments != total_parameters:
                raise Exception(
                    f"Expected {total_parameters} arguments, got {total_arguments}"
                )

            local_namespace = function_kwargs.get("namespace", {})
            function_namespace = dict(zip(parameters, function_args))
            namespace = {**global_namespace, **local_namespace, **function_namespace}

            return self.value.execute(namespace=HashableDict(namespace))

        return function


class Call:
    kind: str = "Call"
    callee: "Term"
    arguments: list["Term"]
    location: Location

    def __init__(self, callee: "Term", arguments: list["Term"], **kwargs):
        self.callee = callee
        self.arguments = arguments

    def execute(self, **kwargs):
        arguments = list(
            map(lambda argument: argument.execute(**kwargs), self.arguments)
        )

        return self.callee.execute(**kwargs)(*arguments, **kwargs)


class Let:
    kind: str = "Let"
    name: Parameter
    value: "Term"
    next: "Term"
    location: Location

    def __init__(self, name: Parameter, value: "Term", **kwargs):
        self.name = name
        self.value = value
        self.next: "Term" = kwargs[
            "next"
        ]  # to avoid shadowing the built-in `next` function

    def execute(self, **kwargs):
        global_namespace = kwargs.get("namespace", {})
        local_namespace = {self.name.text: self.value.execute(**kwargs)}
        namespace = {**global_namespace, **local_namespace}

        return self.next.execute(namespace=HashableDict(namespace))


class Str:
    kind: str = "Str"
    value: str
    location: Location

    def __init__(self, value: str, **kwargs):
        self.value = value

    def execute(self, **kwargs):
        return str(self.value)


class Int:
    kind: str = "Int"
    value: int
    location: Location

    def __init__(self, value: int, **kwargs):
        self.value = value

    def execute(self, **kwargs):
        return int(self.value)


class BinaryOp(Enum):
    Add = "Add"
    Sub = "Sub"
    Mul = "Mul"
    Div = "Div"
    Rem = "Rem"
    Eq = "Eq"
    Neq = "Neq"
    Lt = "Lt"
    Gt = "Gt"
    Lte = "Lte"
    Gte = "Gte"
    And = "And"
    Or = "Or"


class Bool:
    kind: str = "Bool"
    value: bool
    location: Location

    def __init__(self, value: bool, **kwargs):
        self.value = value

    def execute(self, **kwargs):
        return bool(self.value)


class If:
    kind: str = "If"
    condition: "Term"
    then: "Term"
    otherwise: "Term"
    location: Location

    def __init__(self, condition: "Term", then: "Term", otherwise: "Term", **kwargs):
        self.condition = condition
        self.then = then
        self.otherwise = otherwise

    def execute(self, **kwargs):
        if self.condition.execute(**kwargs):
            return self.then.execute(**kwargs)

        return self.otherwise.execute(**kwargs)


class Binary:
    kind: str = "Binary"
    lhs: "Term"
    op: BinaryOp
    rhs: "Term"
    location: Location

    def __init__(self, lhs: "Term", op: BinaryOp, rhs: "Term", **kwargs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs

    def execute(self, **kwargs):
        operator = SUPPORTED_BINARY_OPERATIONS[self.op.name]
        left = self.lhs.execute(**kwargs)
        right = self.rhs.execute(**kwargs)

        return operator(left, right)


class Tuple:
    kind: str = "Tuple"
    first: "Term"
    second: "Term"
    location: Location

    def __init__(self, first: "Term", second: "Term", **kwargs):
        self.first = first
        self.second = second

    def execute(self, **kwargs):
        return self.first.execute(**kwargs), self.second.execute(**kwargs)


class First:
    kind: str = "First"
    value: "Term"
    location: Location

    def __init__(self, value: "Term", **kwargs):
        self.value = value

    def execute(self, **kwargs):
        result = self.value.execute(**kwargs)

        if not isinstance(result, tuple):
            raise RuntimeError(f"Expected a tuple, given {type(result)}")

        first, _ = result

        return first


class Second:
    kind: str = "Second"
    value: "Term"
    location: Location

    def __init__(self, value: "Term", **kwargs):
        self.value = value

    def execute(self, **kwargs):
        result = self.value.execute(**kwargs)

        if not isinstance(result, tuple):
            raise RuntimeError(f"Expected a tuple, given {type(result)}")

        _, second = result

        return second


class Print:
    kind: str = "Print"
    value: "Term"
    location: Location

    def __init__(self, value: "Term", **kwargs):
        self.value = value

    def execute(self, **kwargs):
        result = self.value.execute(**kwargs)

        if isinstance(self.value, Function):
            print("<#closure>")
        else:
            print(result)

        return result


class File:
    name: str = "File"
    expression: "Term"
    location: Location

    def __init__(self, expression: "Term", **kwargs):
        self.expression = expression

    def execute(self, **kwargs):
        return self.expression.execute()


Term = (
    Var
    | Function
    | Call
    | Let
    | Str
    | Int
    | Bool
    | If
    | Binary
    | Tuple
    | First
    | Second
    | Print
)


SUPPORTED_BINARY_OPERATIONS = {
    BinaryOp.Add.name: binary_operations.add,
    BinaryOp.Sub.name: binary_operations.sub,
    BinaryOp.Mul.name: binary_operations.mul,
    BinaryOp.Div.name: binary_operations.div,
    BinaryOp.Rem.name: binary_operations.rem,
    BinaryOp.Eq.name: binary_operations.eq,
    BinaryOp.Neq.name: binary_operations.neq,
    BinaryOp.Lt.name: binary_operations.lt,
    BinaryOp.Gt.name: binary_operations.gt,
    BinaryOp.Lte.name: binary_operations.lte,
    BinaryOp.Gte.name: binary_operations.gte,
    BinaryOp.And.name: binary_operations.and_,
    BinaryOp.Or.name: binary_operations.or_,
}
