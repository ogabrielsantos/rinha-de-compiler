from precisely import assert_that, all_elements, is_instance, has_attrs, is_sequence, mapping_includes

from nodes import Parameter
from utils import with_parameters


class TestWithParameters:
    def test_should_return_empty_list_when_no_parameters(self):
        data = {}

        result = with_parameters(data)

        assert result.get("parameters", {}) == []

    def test_should_convert_parameters_to_parameter_instances(self):
        data = {"parameters": [{"text": "a"}, {"text": "b"}]}

        result = with_parameters(data)
        result_parameters = result.get("parameters", {})

        assert_that(result_parameters, all_elements(is_instance(Parameter)))
        assert_that(result_parameters, is_sequence(
            has_attrs(text="a"),
            has_attrs(text="b"),
        ))

    def test_should_keep_other_fields(self):
        data = {"parameters": [{"text": "a"}, {"text": "b"}], "value": "value"}

        result = with_parameters(data)

        assert_that(result, mapping_includes({
            "value": "value"
        }))
