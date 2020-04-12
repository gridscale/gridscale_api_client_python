from gs_api_client import Configuration, SyncGridscaleApiClient


def test_get_servers(client, mocker):
    mock_api = mocker.patch.object(client.api_client, "call_api")
    mock_api.return_value = (mocker.ANY, 200, None)

    client.get_servers()

    mock_api.assert_called_once_with(
        "/objects/servers",
        "GET",
        mocker.ANY,
        mocker.ANY,
        mocker.ANY,
        body=mocker.ANY,
        post_params=mocker.ANY,
        files=mocker.ANY,
        response_type=mocker.ANY,
        auth_settings=mocker.ANY,
        async_req=mocker.ANY,
        _return_http_data_only=mocker.ANY,
        collection_formats=mocker.ANY,
        _preload_content=mocker.ANY,
        _request_timeout=mocker.ANY,
    )
