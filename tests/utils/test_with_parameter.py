from precisely import (all_elements, assert_that, has_attrs, is_instance,
                       is_sequence, mapping_includes)

from nodes import Parameter
from utils import with_parameter


class TestWithParameter:
    def test_should_convert_parameter_to_parameter_instances(self):
        data = {"name": {"text": "foo"}}

        result = with_parameter(data)
        result_parameter = result["name"]

        assert_that(result_parameter, is_instance(Parameter))
        assert_that(result_parameter, has_attrs(text="foo"))

    def test_should_keep_other_fields(self):
        data = {"name": {"text": "foo"}, "value": "value"}

        result = with_parameter(data)

        assert_that(result, mapping_includes({"value": "value"}))
