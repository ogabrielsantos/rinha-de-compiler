from nodes import File, Str


class TestFile:
    def test_should_return_expected_value(self):
        result = File(
            Str("Hello, World!"),
        ).execute()

        assert result == "Hello, World!"
