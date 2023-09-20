from precisely import assert_that, is_instance, mapping_includes

from nodes import BinaryOp
from utils import with_binary_operation


class TestWithBinaryOperation:
    def test_should_convert_operation_name_to_operation_instances(self):
        data = {"op": BinaryOp.Add}

        result = with_binary_operation(data)
        result_op = result["op"]

        assert_that(result_op, is_instance(BinaryOp))

    def test_should_keep_other_fields(self):
        data = {"op": BinaryOp.Add, "value": "value"}

        result = with_binary_operation(data)

        assert_that(result, mapping_includes({
            "value": "value"
        }))
