import pytest
from src.config.helper import load_config


@pytest.fixture(scope='session')
@load_config
def my_config_loader():
    pass
