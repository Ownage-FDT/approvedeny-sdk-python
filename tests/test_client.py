import json
import hashlib
import hmac
from unittest.mock import patch
import pytest
import requests_mock
from client import Client

API_KEY = 'test-api-key'

@pytest.fixture
def mock_client():
    return Client(api_key=API_KEY)

def test_init_with_api_key():
    client = Client(api_key=API_KEY)
    assert client.base_url == 'https://api.approvedeny.com'
    assert client.headers['Authorization'] == f'Bearer {API_KEY}'
    assert client.headers['Accept'] == 'application/json'
    assert client.headers['Content-Type'] == 'application/json'

def test_init_without_api_key():
    with pytest.raises(ValueError):
        Client(api_key='')

def test_should_return_check_request_data(mock_client):
    check_request_id = 'check-request-id'
    expected_data = {'id': check_request_id, 'description': 'a test description' }
    
    with requests_mock.Mocker() as mocker:
        mocker.get('https://api.approvedeny.com/v1/requests/' + check_request_id , json={ 'data': expected_data}, status_code=200)
        response = mock_client.get_check_request(check_request_id)
    
    assert response['data'] == expected_data

def test_should_throw_an_exception_if_check_request_does_not_exits(mock_client):
    check_request_id = 'check-request-id'
    expected_error_message = 'check request not found'

    with requests_mock.Mocker() as mocker:
        mocker.get('https://api.approvedeny.com/v1/requests/' + check_request_id , json={'message': expected_error_message }, status_code=404)
        with pytest.raises(Exception):
            mock_client.get_check_request(check_request_id)

def test_should_create_a_check_request(mock_client):
    check_id = 'check-id'
    payload = { 'description': 'a test description', 'metadata': { 'test': 'true' } }
    expected_data = { 'id': 'check-request-id', **payload }

    with requests_mock.Mocker() as mocker:
        mocker.post('https://api.approvedeny.com/v1/checks/' + check_id , json={ 'data': expected_data }, status_code=200)
        response = mock_client.create_check_request(check_id, payload)

    assert response['data'] == expected_data

def test_should_throw_an_exception_if_check_does_not_exits(mock_client):
    check_id = 'invalid-check-id'
    payload = { 'description': 'a test description', 'metadata': { 'test': 'true' } }
    expected_error_message = 'check not found'

    with requests_mock.Mocker() as mocker:
        mocker.post('https://api.approvedeny.com/v1/checks/' + check_id , json={ 'message': expected_error_message }, status_code=404)
        with pytest.raises(Exception):
            mock_client.create_check_request(check_id, payload)

def test_should_return_check_request_response(mock_client):
    check_request_id = 'check-request-id'
    expected_data = { 'id': check_request_id, 'status': 'approved' }

    with requests_mock.Mocker() as mocker:
        mocker.get('https://api.approvedeny.com/v1/requests/' + check_request_id + '/response', json={ 'data': expected_data }, status_code=200)
        response = mock_client.get_check_request_response(check_request_id)

    assert response['data'] == expected_data

def test_should_throw_an_exception_if_check_request_response_does_not_exits(mock_client):
    check_request_id = 'check-request-id'
    expected_error_message = 'check request not found'

    with requests_mock.Mocker() as mocker:
        mocker.get('https://api.approvedeny.com/v1/requests/' + check_request_id + '/response', json={ 'message': expected_error_message }, status_code=404)
        with pytest.raises(Exception):
            mock_client.get_check_request_response(check_request_id)


def test_should_return_true_if_webhook_signature_is_valid(mock_client):
    encryption_key = 'encryption_key'
    payload = {'event': 'response.created', 'data': { 'id': 'test-id' } }

    signature = hmac.new(encryption_key.encode('utf-8'), json.dumps(payload).encode('utf-8'), hashlib.sha256).hexdigest()

    assert mock_client.is_valid_webhook_signature(encryption_key, signature, payload)

def test_is_valid_webhook_signature_invalid(mock_client):
    assert not mock_client.is_valid_webhook_signature('key', 'invalid_signature', {})