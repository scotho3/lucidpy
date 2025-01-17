import pytest

from lucidpy.client import LucidchartClient


@pytest.fixture
def client():
    return LucidchartClient(api_key="test-api-key")


def test_create_document_with_json(client, mocker):
    mock_response = mocker.patch.object(
        client, "_make_request", return_value={"id": "doc1"}
    )
    response = client.create_document(title="Test Document", json='{"key": "value"}')
    assert response["id"] == "doc1"
    mock_response.assert_called_once_with("POST", "/documents", files=mocker.ANY)


def test_create_document_with_document(client, mocker):
    mock_response = mocker.patch.object(
        client, "_make_request", return_value={"id": "doc1"}
    )
    mock_document = mocker.Mock()
    mock_document.model_dump_json.return_value = '{"key": "value"}'
    response = client.create_document(title="Test Document", document=mock_document)
    assert response["id"] == "doc1"
    mock_response.assert_called_once_with("POST", "/documents", files=mocker.ANY)
