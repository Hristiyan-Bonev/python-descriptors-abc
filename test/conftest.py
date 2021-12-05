import pytest

from models.base import BaseModel

@pytest.fixture(scope="function")
def base_model():
    def _inner(model_properties):
        return type("model", (BaseModel,), model_properties)
    return _inner