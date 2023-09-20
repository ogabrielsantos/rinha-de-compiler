from unittest.mock import patch

import pytest

from nodes import Print, Str, Var, Int, Bool, Tuple, Function


class TestPrint:
    @patch("nodes.print")
    @pytest.mark.parametrize(
        "value, expected_message",
        [
            [Var("foo"), "foo value"],
            [Str("foo"), "foo"],
            [Int(20), 20],
            [Bool(True), True],
            # [Function(parameters=[], value=Int(10)), "<function>"], @todo case not clear
            [Tuple(Int(10), Int(20)), (10, 20)],
        ]
    )
    def test_should_print_sent_value(self, mock_print, value, expected_message):
        Print(value).execute(namespace={"foo": "foo value"})

        mock_print.assert_called_with(expected_message)
