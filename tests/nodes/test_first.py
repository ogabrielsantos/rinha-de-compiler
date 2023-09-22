import pytest

from nodes import First, Int, Tuple, Var, HashableDict


class TestFirst:
    def test_should_return_expected_value(self):
        result = First(
            Tuple(
                Int(10),
                Int(20),
            )
        ).execute()

        assert result == 10

    def test_should_raise_exception_when_is_not_a_tuple(self):
        with pytest.raises(RuntimeError):
            First(Int(10)).execute()

    def test_should_keep_namespace_values(self):
        result = First(
            Tuple(
                Var("foo"),
                Var("bar"),
            )
        ).execute(namespace=HashableDict({"foo": "foo value", "bar": "bar value"}))

        assert result == "foo value"
