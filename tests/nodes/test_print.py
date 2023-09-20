from types import FunctionType
from unittest.mock import patch, call

import pytest

from nodes import Print, Str, Var, Int, Bool, Tuple, Function, Let, Parameter, Call, Binary, BinaryOp, File


class TestPrint:
    @patch("nodes.print")
    @pytest.mark.parametrize(
        "value, expected_message",
        [
            [Var("foo"), "foo value"],
            [Str("foo"), "foo"],
            [Int(20), 20],
            [Bool(True), True],
            [Function(parameters=[], value=Int(10)), "<#closure>"],
            [Tuple(Int(10), Int(20)), (10, 20)],
            [Tuple(Str("foo"), Str("bar")), ("foo", "bar")],
        ]
    )
    def test_should_print_sent_value(self, mock_print, value, expected_message):
        Print(value).execute(namespace={"foo": "foo value"})

        mock_print.assert_called_with(expected_message)

    @patch("nodes.print")
    @pytest.mark.parametrize(
        "value, expected_messages",
        [
            [
                Let(
                    name=Parameter("_"),
                    value=Print(Int(1)),
                    next=Print(Int(2))
                ),
                [call(1), call(2)]
            ],
            [
                Call(
                    callee=Function(
                        parameters=[
                            Parameter("a"),
                            Parameter("b"),
                            Parameter("c")
                        ],
                        value=Str("foo")
                    ),
                    arguments=[
                        Print(Int(1)),
                        Print(Int(2)),
                        Print(Int(3))
                    ]
                ),
                [call(1), call(2), call(3)]
            ],
            [
                Let(
                    name=Parameter("tuple"),
                    value=Tuple(
                        Print(Int(1)),
                        Print(Int(2)),
                    ),
                    next=Print(Var("tuple"))
                ),
                [call(1), call(2), call((1, 2))]
            ],
            [
                Print(
                    Binary(
                        lhs=Print(Int(1)),
                        op=BinaryOp.Add,
                        rhs=Print(Int(2)),
                    )
                ),
                [call(1), call(2), call(3)]
            ]
        ]
    )
    def test_should_print_complex_values(self, mock_print, value, expected_messages):
        File(expression=value).execute()

        mock_print.assert_has_calls(expected_messages, any_order=False)

    @patch("nodes.print")
    @pytest.mark.parametrize(
        "value, expected_value",
        [
            [Var("foo"), "foo value"],
            [Str("foo"), "foo"],
            [Int(20), 20],
            [Bool(True), True],
            [Tuple(Int(10), Int(20)), (10, 20)],
            [Tuple(Str("foo"), Str("bar")), ("foo", "bar")],
        ]
    )
    def test_should_return_value(self, mock_print, value, expected_value):
        result = Print(value).execute(namespace={"foo": "foo value"})

        assert result == expected_value

    @patch("nodes.print")
    def test_should_return_function(self, mock_print):
        function = Function(parameters=[], value=Int(10))
        result = Print(function).execute()

        assert isinstance(result, FunctionType)
