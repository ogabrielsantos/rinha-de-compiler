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
    If,
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

    def test_should_not_overwrite_scoped_variables(self):
        """
        let foo = (n1Fn, n2Fn) => {
            let n1 = n1Fn();
            let k2 = n2Fn();

            if (n1 == 5) {
                return n1
            } else {
                return foo(() => n2, () => n1 + n2)
            }
        };
        foo(() => 0, () => 1)
        """
        result = Let(
            name=Parameter(text="foo"),
            value=Function(
                parameters=[
                    Parameter(text="n1Fn"),
                    Parameter(text="n2Fn"),
                ],
                value=Let(
                    name=Parameter(text="n1"),
                    value=Call(
                        callee=Var("n1Fn"),
                        arguments=[],
                    ),
                    next=Let(
                        name=Parameter(text="n2"),
                        value=Call(
                            callee=Var("n2Fn"),
                            arguments=[],
                        ),
                        next=If(
                            condition=Binary(
                                Var("n1"),
                                BinaryOp.Eq,
                                Int(5),
                            ),
                            then=Var("n1"),
                            otherwise=Call(
                                callee=Var("foo"),
                                arguments=[
                                    Function(
                                        parameters=[],
                                        value=Var("n2"),
                                    ),
                                    Function(
                                        parameters=[],
                                        value=Binary(
                                            Var("n1"),
                                            BinaryOp.Add,
                                            Var("n2"),
                                        ),
                                    ),
                                ],
                            ),
                        ),
                    ),
                ),
            ),
            next=Call(
                callee=Var("foo"),
                arguments=[
                    Function(
                        parameters=[],
                        value=Int(0),
                    ),
                    Function(
                        parameters=[],
                        value=Int(1),
                    ),
                ],
            ),
        ).execute()

        assert result == 5
