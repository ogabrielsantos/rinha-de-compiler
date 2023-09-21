import pytest
from precisely import all_elements, assert_that, is_instance

from nodes import (Binary, BinaryOp, Bool, Call, First, Function, If, Int, Let,
                   Parameter, Print, Second, Str, Tuple, Var)
from utils import to_ast_node


class TestToAstNode:
    def test_should_not_modify_if_not_a_node(self):
        assert to_ast_node({}) == {}

    def test_should_not_modify_if_is_an_unsupported_node(self):
        assert to_ast_node({"kind": "Unsupported"}) == {"kind": "Unsupported"}

    @pytest.mark.parametrize(
        "data, expected_instance",
        [
            [{"kind": Var.kind, "text": "foo"}, Var],
            [{"kind": Function.kind, "parameters": [], "value": "foo"}, Function],
            [{"kind": Call.kind, "callee": "foo", "arguments": []}, Call],
            [
                {
                    "kind": Let.kind,
                    "name": {"text": "foo"},
                    "value": "bar",
                    "next": None,
                },
                Let,
            ],
            [{"kind": Str.kind, "value": "foo"}, Str],
            [{"kind": Int.kind, "value": 1}, Int],
            [{"kind": Bool.kind, "value": True}, Bool],
            [
                {
                    "kind": If.kind,
                    "condition": "foo",
                    "then": "foo",
                    "otherwise": "foo",
                },
                If,
            ],
            [
                {"kind": Binary.kind, "lhs": "foo", "op": BinaryOp.Eq, "rhs": "foo"},
                Binary,
            ],
            [{"kind": Tuple.kind, "first": 10, "second": 20}, Tuple],
            [{"kind": First.kind, "value": (10, 20)}, First],
            [{"kind": Second.kind, "value": (10, 20)}, Second],
            [{"kind": Print.kind, "value": "foo"}, Print],
        ],
    )
    def test_should_return_kind_instance_if_is_a_supported_node(
        self, data, expected_instance
    ):
        result = to_ast_node(data)

        assert isinstance(result, expected_instance)

    def test_should_convert_op_to_binary_op(self):
        result = to_ast_node(
            {"kind": Binary.kind, "lhs": "foo", "op": "Eq", "rhs": "foo"}
        )

        assert isinstance(result.op, BinaryOp)

    def test_should_convert_name_to_parameter(self):
        result = to_ast_node(
            {"kind": Let.kind, "name": {"text": "foo"}, "value": "bar", "next": None}
        )

        assert isinstance(result.name, Parameter)

    def test_should_convert_parameters_to_parameter_instances(self):
        result = to_ast_node(
            {
                "kind": Function.kind,
                "parameters": [{"text": "foo"}, {"text": "bar"}],
                "value": "foo",
            }
        )

        assert_that(result.parameters, all_elements(is_instance(Parameter)))
