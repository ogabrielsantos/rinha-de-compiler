from nodes import Call, Function, Parameter, Binary, BinaryOp, Var, Int


class TestCall:
    def test_should_return_expected_value(self):
        callee = Function(
            parameters=[
                Parameter(text="foo"),
                Parameter(text="bar"),
            ],
            value=Binary(
                Var("foo"),
                BinaryOp.Add,
                Var("bar"),
            ),
        )
        result = Call(
            callee=callee,
            arguments=[
                Int(100),
                Int(200),
            ],
        ).execute()

        assert result == 300
