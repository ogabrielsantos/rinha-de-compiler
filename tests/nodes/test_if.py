from nodes import If, Binary, Int, BinaryOp, Str, Bool, Var


class TestIf:
    def test_should_return_expected_value_when_true(self):
        result = If(
            condition=Binary(
                Int(10),
                BinaryOp.Eq,
                Int(10)
            ),
            then=Bool(True),
            otherwise=Bool(False)
        ).execute()

        assert result is True

    def test_should_return_expected_value_when_false(self):
        result = If(
            condition=Binary(
                Int(33),
                BinaryOp.Eq,
                Int(10)
            ),
            then=Bool(True),
            otherwise=Bool(False)
        ).execute()

        assert result is False

    def test_should_keep_namespace_values(self):
        result = If(
            condition=Binary(
                Int(10),
                BinaryOp.Eq,
                Int(10)
            ),
            then=Var("foo"),
            otherwise=Var("bar")
        ).execute(namespace={"foo": "foo value", "bar": "bar value"})

        assert result == "foo value"
