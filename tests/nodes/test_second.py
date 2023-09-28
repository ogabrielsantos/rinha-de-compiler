import pytest

from nodes import Int, Second, Tuple, Var, HashableDict


class TestSecond:
    def test_should_return_expected_value(self):
        result = Second(
            Tuple(
                Int(10),
                Int(20),
            )
        ).execute()

        assert result == 20

    def test_should_raise_exception_when_is_not_a_tuple(self):
        with pytest.raises(RuntimeError):
            Second(Int(10)).execute()

    def test_should_keep_namespace_values(self):
        result = Second(
            Tuple(
                Var("foo"),
                Var("bar"),
            )
        ).execute(namespace=HashableDict({"foo": "foo value", "bar": "bar value"}))

        assert result == "bar value"

    def test_should_allow_nested_calls(self):
        result = Second(
            Second(
                Tuple(
                    Int(10),
                    Tuple(
                        Int(20),
                        Int(30),
                    ),
                )
            ),
        ).execute()

        assert result == 30
