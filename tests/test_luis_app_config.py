from app_config import DefaultConfig

CONFIG = DefaultConfig()

def test_authoring_key():
    assert CONFIG.AUTHORING_KEY != ""


def test_authoring_endpoint():
    assert CONFIG.AUTHORING_ENDPOINT != ""


def test_prediction_key():
    assert CONFIG.PREDICTION_KEY != ""


def test_prediction_endpoint():
    assert CONFIG.PREDICTION_ENDPOINT != ""
