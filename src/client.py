import requests
import hashlib
import hmac
import json
from typing import Dict, Any, Union

class Client:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("The Approvedeny SDK requires an API key to be provided at initialization")
        
        self.base_url = 'https://api.approvedeny.com'
        self.headers = {
            'Authorization': f'Bearer {api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'approvedeny-python/1.0.0'
        }

    def _make_request(self, method: str, endpoint: str, data: Union[None, dict] = None):
        response = requests.request(
            method,
            f'{self.base_url}{endpoint}',
            headers=self.headers,
            json=data
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}")

    def get_check_request(self, check_request_id: str):
        endpoint = f'/v1/requests/{check_request_id}'
        return self._make_request('GET', endpoint)

    def create_check_request(self, check_id: str, payload: dict):
        endpoint = f'/v1/checks/{check_id}'
        return self._make_request('POST', endpoint, payload)

    def get_check_request_response(self, check_request_id: str):
        endpoint = f'/v1/requests/{check_request_id}/response'
        return self._make_request('GET', endpoint)

    def is_valid_webhook_signature(self, encryption_key: str, signature: str, payload: dict):
        hmac_calculated = hmac.new(
            encryption_key.encode('utf-8'),
            json.dumps(payload).encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(hmac_calculated, signature)

    @staticmethod
    def parse_error_message(error_response: Dict[str, Any]) -> str:
        return error_response.get('message', 'An error occurred')
