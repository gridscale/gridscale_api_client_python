import os.path

from gs_api_client import Configuration
from examples.configloader import load_config


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

def test_debug_is_disabled_by_default():
    config = Configuration()
    assert not config.debug


def test_tls_certs_are_verified_by_default():
    config = Configuration()
    assert config.verify_ssl


def test_load_config_from_yaml():
    """"Make sure we can load a config from a given YAML file."""

    example_config = os.path.join(CURRENT_DIR, "example-config.yaml")
    res = load_config(example_config)
    assert isinstance(res, list)
    assert len(res) == 2
    assert res[0]["name"] == "default"
    assert res[1]["name"] == "something-else"
