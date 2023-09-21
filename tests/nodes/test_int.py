import pytest
from precisely import assert_that, equal_to, is_instance

from nodes import Int


class TestInt:
    @pytest.mark.parametrize(
        "value, expected_value",
        [
            [1, 1],
            [10, 10],
            [30.5, 30],
        ],
    )
    def test_should_return_value_as_int(self, value: int | float, expected_value):
        result = Int(value).execute()

        assert_that(result, is_instance(int))
        assert_that(result, equal_to(expected_value))
