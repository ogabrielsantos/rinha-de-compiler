from types import FunctionType

import pytest

from nodes import (
    Binary,
    BinaryOp,
    Function,
    Parameter,
    Var,
    Let,
    Int,
    Print,
    Call,
    HashableDict,
)


class TestFunction:
    def test_should_return_a_function(self):
        result = Function(
            parameters=[
                Parameter(text="foo"),
                Parameter(text="bar"),
            ],
            value=Binary(
                Var("foo"),
                BinaryOp.Add,
                Var("bar"),
            ),
        ).execute()

        assert isinstance(result.__wrapped__, FunctionType)

    def test_should_return_a_function_that_executes_expected_term(self):
        result = Function(
            parameters=[
                Parameter(text="foo"),
                Parameter(text="bar"),
            ],
            value=Binary(
                Var("foo"),
                BinaryOp.Add,
                Var("bar"),
            ),
        ).execute()

        assert result(100, 200) == 300

    def test_should_raise_an_exception_if_function_is_called_with_wrong_number_of_parameters(
        self,
    ):
        result = Function(
            parameters=[
                Parameter(text="foo"),
                Parameter(text="bar"),
            ],
            value=Binary(
                Var("foo"),
                BinaryOp.Add,
                Var("bar"),
            ),
        ).execute()

        with pytest.raises(Exception):
            result(100)

    def test_should_allow_usage_of_variables_from_namespace(self):
        result = Function(
            parameters=[
                Parameter(text="foo"),
            ],
            value=Binary(
                Var("foo"),
                BinaryOp.Add,
                Var("bar"),
            ),
        ).execute()

        assert result(100, namespace=HashableDict({"bar": 200})) == 300

    def test_should_overwrite_variables_from_namespace(self):
        result = Function(
            parameters=[
                Parameter(text="foo"),
                Parameter(text="bar"),
            ],
            value=Binary(
                Var("foo"),
                BinaryOp.Add,
                Var("bar"),
            ),
        ).execute()

        assert result(100, 500, namespace=HashableDict({"bar": 200})) == 600

    def test_should_allow_usage_of_variables_from_local_namespace(self):
        result = Let(
            name=Parameter(text="a"),
            value=Int(9),
            next=Let(
                name=Parameter(text="test"),
                value=Function(
                    parameters=[],
                    value=Let(
                        name=Parameter(text="d"),
                        value=Int(10),
                        next=Let(
                            name=Parameter(text="closure"),
                            value=Function(
                                parameters=[Parameter(text="n")],
                                value=Binary(
                                    Binary(
                                        Var("n"),
                                        BinaryOp.Mul,
                                        Var("d"),
                                    ),
                                    BinaryOp.Add,
                                    Var("a"),
                                ),
                            ),
                            next=Var("closure"),
                        ),
                    ),
                ),
                next=Print(
                    Call(
                        callee=Call(
                            callee=Var("test"),
                            arguments=[],
                        ),
                        arguments=[
                            Int(5),
                        ],
                    )
                ),
            ),
        ).execute()

        assert result == 59
