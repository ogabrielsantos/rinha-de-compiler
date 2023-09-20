from nodes import Var


class TestVar:
    def test_should_return_value_from_namespace(self):
        result = Var("foo").execute(namespace={"foo": "bar"})

        assert result == "bar"

    def test_should_return_nothing_when_variable_doesnt_exist(self):
        result = Var("foo").execute(namespace={})

        assert result is None

    def test_should_return_nothing_when_namespace_not_provided(self):
        result = Var("foo").execute()

        assert result is None
