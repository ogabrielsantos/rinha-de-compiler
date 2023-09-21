import pytest

from nodes import Binary, BinaryOp, Bool, Int, Str


class TestBinary:
    @pytest.mark.parametrize(
        "operation, left, right, expected_result",
        [
            [BinaryOp.Add, Int(3), Int(5), 8],
            [BinaryOp.Add, Str("a"), Int(2), "a2"],
            [BinaryOp.Add, Int(2), Str("a"), "2a"],
            [BinaryOp.Add, Str("a"), Str("b"), "ab"],
            [BinaryOp.Sub, Int(10), Int(1), 9],
            [BinaryOp.Sub, Int(0), Int(1), -1],
            [BinaryOp.Sub, Int(10), Int(-1), 11],
            [BinaryOp.Mul, Int(2), Int(2), 4],
            [BinaryOp.Div, Int(3), Int(2), 1],
            [BinaryOp.Rem, Int(4), Int(2), 0],
            [BinaryOp.Eq, Str("a"), Str("a"), True],
            [BinaryOp.Eq, Int(2), Binary(Int(1), BinaryOp.Add, Int(1)), True],
            [BinaryOp.Eq, Int(2), Int(1), False],
            [BinaryOp.Eq, Bool(True), Bool(True), True],
            [BinaryOp.Neq, Str("a"), Str("b"), True],
            [BinaryOp.Neq, Int(3), Binary(Int(1), BinaryOp.Add, Int(1)), True],
            [BinaryOp.Neq, Int(3), Int(3), False],
            [BinaryOp.Neq, Bool(True), Bool(False), True],
            [BinaryOp.Lt, Int(1), Int(2), True],
            [BinaryOp.Lt, Int(3), Int(2), False],
            [BinaryOp.Lt, Int(2), Int(2), False],
            [BinaryOp.Gt, Int(2), Int(3), False],
            [BinaryOp.Gt, Int(3), Int(3), False],
            [BinaryOp.Gt, Int(5), Int(3), True],
            [BinaryOp.Lte, Int(1), Int(2), True],
            [BinaryOp.Lte, Int(3), Int(2), False],
            [BinaryOp.Lte, Int(2), Int(2), True],
            [BinaryOp.Gte, Int(2), Int(3), False],
            [BinaryOp.Gte, Int(3), Int(3), True],
            [BinaryOp.Gte, Int(5), Int(3), True],
            [BinaryOp.And, Bool(True), Bool(True), True],
            [BinaryOp.And, Bool(True), Bool(False), False],
            [BinaryOp.And, Bool(False), Bool(True), False],
            [BinaryOp.And, Bool(False), Bool(False), False],
            [BinaryOp.Or, Bool(True), Bool(True), True],
            [BinaryOp.Or, Bool(True), Bool(False), True],
            [BinaryOp.Or, Bool(False), Bool(True), True],
            [BinaryOp.Or, Bool(False), Bool(False), False],
        ],
    )
    def test_should_return_operator_result(
        self, operation: BinaryOp, left, right, expected_result
    ):
        result = Binary(left, operation, right).execute()

        assert result == expected_result
