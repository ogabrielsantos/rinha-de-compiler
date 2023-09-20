def add(x, y):
    if type(x) == str or type(y) == str:
        return str(x) + str(y)

    return x + y


def sub(x, y):
    return x - y


def mul(x, y):
    return x * y


def div(x, y):
    return int(x / y)


def rem(x, y):
    return x % y


def eq(x, y):
    return x == y


def neq(x, y):
    return x != y


def lt(x, y):
    return x < y


def gt(x, y):
    return x > y


def lte(x, y):
    return x <= y


def gte(x, y):
    return x >= y


def and_(x, y):
    return x and y


def or_(x, y):
    return x or y
