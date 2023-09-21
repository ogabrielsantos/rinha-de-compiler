from nodes import Str, Tuple, Var


class TestTuple:
    def test_should_return_expected_values(self):
        result = Tuple(
            first=Str("Hello"),
            second=Str("World"),
        ).execute()

        assert result == ("Hello", "World")

    def test_should_keep_namespace_values(self):
        result = Tuple(
            first=Var("foo"),
            second=Var("bar"),
        ).execute(namespace={"foo": "Hello", "bar": "World"})

        assert result == ("Hello", "World")
