from gs_api_client import Configuration


def test_debug_is_disabled_by_default():
    config = Configuration()
    assert not config.debug


def test_tls_certs_are_verified_by_default():
    config = Configuration()
    assert config.verify_ssl
