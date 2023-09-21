from unittest.mock import patch

from nodes import Let, Parameter, Print, Str, Var


class TestLet:
    @patch("nodes.print")
    def test_should_send_variable_with_desired_value_to_next_term(self, mock_print):
        Let(
            name=Parameter("value"), value=Str("foo"), next=Print(Var("value"))
        ).execute()

        mock_print.assert_called_with("foo")

    @patch("nodes.print")
    def test_should_keep_namespace_values(self, mock_print):
        Let(
            name=Parameter("value"),
            value=Str("foo"),
            next=Print(Var("bar")),
        ).execute(namespace={"bar": "global value"})

        mock_print.assert_called_with("global value")

    @patch("nodes.print")
    def test_should_overwrite_namespace_value(self, mock_print):
        Let(
            name=Parameter("value"),
            value=Str("local value"),
            next=Print(Var("value")),
        ).execute(namespace={"value": "global value"})

        mock_print.assert_called_with("local value")
