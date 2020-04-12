from typing import Iterator

import pytest

from gs_api_client import SyncGridscaleApiClient, Configuration


@pytest.fixture
def client() -> Iterator[SyncGridscaleApiClient]:
    """Fixture that creates and configures a synchronous API client."""

    c = Configuration()
    c.host = "https://example.com"
    c.api_key["X-Auth-Token"] = "fake-token"
    c.api_key["X-Auth-UserId"] = "not-a-uuid"

    yield SyncGridscaleApiClient(configuration=c)
