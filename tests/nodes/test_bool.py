import pytest

from nodes import Bool


class TestBool:
    @pytest.mark.parametrize(
        "value, expected_value",
        [
            [True, True],
            [False, False],
            ["foo", True],
            ["", False],
            [0, False],
            [None, False],
        ],
    )
    def test_should_handle_truly_and_falsy_values(
        self, value: str | int | bool, expected_value
    ):
        assert Bool(value).execute() == expected_value
