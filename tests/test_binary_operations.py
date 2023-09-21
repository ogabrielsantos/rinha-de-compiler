import pytest

import binary_operations


class TestBinaryOperations:
    @pytest.mark.parametrize(
        "operation, left, right, expected",
        [
            [binary_operations.add, 3, 5, 8],
            [binary_operations.add, "a", 2, "a2"],
            [binary_operations.add, 2, "a", "2a"],
            [binary_operations.add, "a", "b", "ab"],
            [binary_operations.sub, 10, 1, 9],
            [binary_operations.sub, 0, 1, -1],
            [binary_operations.sub, 10, -1, 11],
            [binary_operations.mul, 2, 2, 4],
            [binary_operations.div, 3, 2, 1],
            [binary_operations.rem, 4, 2, 0],
            [binary_operations.eq, "a", "a", True],
            [binary_operations.eq, 2, 1 + 1, True],
            [binary_operations.eq, 2, 1, False],
            [binary_operations.eq, True, True, True],
            [binary_operations.neq, "a", "b", True],
            [binary_operations.neq, 3, 1 + 1, True],
            [binary_operations.neq, 3, 3, False],
            [binary_operations.neq, True, False, True],
            [binary_operations.lt, 1, 2, True],
            [binary_operations.lt, 3, 2, False],
            [binary_operations.lt, 2, 2, False],
            [binary_operations.gt, 2, 3, False],
            [binary_operations.gt, 3, 3, False],
            [binary_operations.gt, 5, 3, True],
            [binary_operations.lte, 1, 2, True],
            [binary_operations.lte, 3, 2, False],
            [binary_operations.lte, 2, 2, True],
            [binary_operations.gte, 2, 3, False],
            [binary_operations.gte, 3, 3, True],
            [binary_operations.gte, 5, 3, True],
            [binary_operations.and_, True, True, True],
            [binary_operations.and_, True, False, False],
            [binary_operations.and_, False, True, False],
            [binary_operations.and_, False, False, False],
            [binary_operations.or_, True, True, True],
            [binary_operations.or_, True, False, True],
            [binary_operations.or_, False, True, True],
            [binary_operations.or_, False, False, False],
        ],
    )
    def test_should_return_correct_result(
        self, operation: callable, left, right, expected
    ):
        assert operation(left, right) == expected
