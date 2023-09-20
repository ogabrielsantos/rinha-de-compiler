from utils import identity


class TestIdentity:
    def test_should_return_received_parameter(self):
        assert identity(3) == 3

    def test_should_return_received_dict(self):
        data = {"a": 1, "b": 2}

        assert id(identity(data)) == id(data)
