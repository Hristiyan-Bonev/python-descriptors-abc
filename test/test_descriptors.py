from fields.string_field import RegexField, PhoneField
import pytest


@pytest.mark.parametrize('value,expected,descriptor_field, additional_props', [
("0899999999", "0899999999", PhoneField, {"strict":True}),
("", "12345", PhoneField, {"default_value": "12345"}),
])
def test_phone_field_descriptor(value, expected, descriptor_field, additional_props):

    foo = type("Foo", (), {"bar" :descriptor_field(**additional_props)})
    f = foo()
    f.bar =  value
    assert f.bar == expected



@pytest.mark.parametrize('value,expected,error_message', [
("", None, "Value '' does not match regex pattern.*"),
(5, None, "Cannot use <class 'int'>.*")
])
def test_strict_descriptor(value, expected, error_message):

    foo = type("Foo", (), {"bar" :PhoneField(strict=True)})
    with pytest.raises(ValueError, match=error_message):
        f = foo()
        f.bar =  value
        assert f.bar == None


@pytest.mark.parametrize('value,default_value,error_message', [
("", "12345-5431-43134", "Value '' does not match regex pattern.*"),
])
def test_default_value_descriptor(value, default_value, error_message):

    foo = type("Foo", (), {"bar" :PhoneField(default_value=default_value)})
    f = foo()
    f.bar =  value
    assert f.bar == default_value