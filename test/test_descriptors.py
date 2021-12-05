from descriptors.lookup_field import OneOf
from descriptors.regex import PhoneField
import pytest


@pytest.mark.parametrize('value,exception', [
    ("", ValueError),#, match="Value '' does not match regex pattern.*")),
    ("123", ValueError),#, match="Value '123' does not match regex pattern.*")),
    (5, TypeError),#, match="Cannot use value of type int as type str"))
])
def test_bad_descriptor(value, exception, base_model):
    
    model = base_model({"phone": PhoneField()})
    
    obj = model(**{"phone": value})

    assert obj.phone == value
    assert len(obj.errors_list) == 1
    assert obj.errors_list[0]['error_type'] == exception.__name__


@pytest.mark.parametrize('value,default_value', [
    ("", "12345-5431-43134"),
])
def test_default_value_descriptor(value, default_value, base_model):
    model = base_model({"phone": PhoneField(default_value=default_value)})
    obj = model(**{"phone": value})
    assert obj.phone == default_value


@pytest.mark.parametrize('value', [
    "bar", "baz"
])
def test_oneof_field(value,base_model):
    klass = base_model({"desc_attribute": OneOf(
        lookup_values=["foo", "bar", "baz"])})
    f = klass()
    f.desc_attribute = value
    assert f.desc_attribute == value
