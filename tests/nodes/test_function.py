from types import FunctionType

import pytest

from nodes import Binary, BinaryOp, Function, Parameter, Var


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

        assert isinstance(result, FunctionType)

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

        assert result(100, namespace={"bar": 200}) == 300

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

        assert result(100, 500, namespace={"bar": 200}) == 600
