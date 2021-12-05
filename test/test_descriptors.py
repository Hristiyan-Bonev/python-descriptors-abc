from descriptors.lookup_field import OneOf
from descriptors.regex import PhoneField
import pytest
from contextlib import ExitStack as does_not_raise_exception

@pytest.mark.parametrize('value,expected_value, additional_props, expectation', [
    ("0899999999", "0899999999", {}, does_not_raise_exception()),
    ("12345", "12345", {"pattern": "[1-5]{5}"}, does_not_raise_exception()),
    ("", "12345", {"default_value": "12345"}, does_not_raise_exception()),
    ("", None, {"required": True}, pytest.raises(ValueError,
     match="Value '' does not match regex pattern .*"))])
def test_phone_field(value, expected_value, additional_props, expectation):
    with expectation:
        klass = type(
            "klass", (), {"descriptor_field": PhoneField(**additional_props)})
        test_obj = klass()
        test_obj.descriptor_field = value
        assert test_obj.descriptor_field == expected_value

@pytest.mark.parametrize('value,exception', [
    ("", pytest.raises(ValueError, match="Value '' does not match regex pattern.*")),
    ("123", pytest.raises(ValueError, match="Value '123' does not match regex pattern.*")),
    (5, pytest.raises(TypeError, match="Cannot use value of type int as type str"))
])
def test_required_descriptor(value, exception):
    klass = type(
        "klass", (), {"descriptor_attribute": PhoneField(required=True)})
    with exception:
        test_obj = klass()
        test_obj.descriptor_attribute = value
        assert test_obj.descriptor_attribute == None


@pytest.mark.parametrize('value,default_value', [
    ("", "12345-5431-43134"),
])
def test_default_value_descriptor(value, default_value):
    klass = type("klass", (), {"bar": PhoneField(default_value=default_value)})
    f = klass()
    f.bar = value
    assert f.bar == default_value


@pytest.mark.parametrize('value', [
    "bar", "baz"
])
def test_oneof_field(value):
    klass = type("klass", (), {"desc_attribute": OneOf(
        lookup_values=["foo", "bar", "baz"])})
    f = klass()
    f.desc_attribute = value
    assert f.desc_attribute == value
