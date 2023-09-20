from precisely import assert_that, is_instance, equal_to
import pytest

from nodes import Str


class TestStr:
    @pytest.mark.parametrize("value, expected_value", [
        [1,  "1"],
        ["foo", "foo"],
    ])
    def test_should_return_value_as_int(self, value: int | str, expected_value):
        result = Str(value).execute()

        assert_that(result, is_instance(str))
        assert_that(result, equal_to(expected_value))
