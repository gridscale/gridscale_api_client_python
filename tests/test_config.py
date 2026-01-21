import os.path
import shutil

import pytest

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
    """Make sure we can load a config from a given YAML file."""

    example_config = os.path.join(CURRENT_DIR, "example-config.yaml")
    res = load_config(example_config)
    assert isinstance(res, list)
    assert len(res) == 2
    assert isinstance(res[0], dict)
    assert res[0]["name"] == "default"
    assert res[1]["name"] == "something-else"


def test_load_config_works_without_fileext(tmp_path):
    """Ensure load_config does not interpret file path or file name."""

    example_config = os.path.join(CURRENT_DIR, "example-config.yaml")
    dest = tmp_path / "a"
    shutil.copyfile(example_config, dest)
    res = load_config(dest)
    assert isinstance(res, list)
    assert len(res) == 2


def test_load_config_handles_non_existing_file():
    """ "Ensure load_config raises FileNotFoundError."""

    with pytest.raises(FileNotFoundError):
        load_config("fufu.yaml")


def test_load_config_checks_for_bogus_input():
    """ "Ensure load_config checks it's input."""

    with pytest.raises(AssertionError):
        load_config(42)

    with pytest.raises(AssertionError):
        load_config("")


def test_load_config_propagates_parsing_errors():
    """ "Ensure load_config raises any error during parsing."""

    import yaml

    not_a_yaml_file = os.path.join(CURRENT_DIR, "test_config.py")
    with pytest.raises(yaml.YAMLError):
        load_config(not_a_yaml_file)


def test_load_config_has_doc_string():
    """ "Make sure load_config is documented."""

    assert load_config.__doc__
