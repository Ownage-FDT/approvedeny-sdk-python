# ApproveDeny SDK for Python

[![PyPI version](https://badge.fury.io/py/approvedeny.svg)](https://badge.fury.io/py/approvedeny)
[![Downloads](https://pepy.tech/badge/approvedeny)](https://pepy.tech/project/approvedeny)

The ApproveDeny SDK for Python provides an easy way to interact with the ApproveDeny API using Python.

## Installation
> **Requires [Python 3.7+](https://www.python.org/downloads/)**

You can install the package via pip:

```bash
pip install approvedeny
```

## Usage
To use the SDK, you need to create an instance of the Client class. You can do this by passing your API key to the constructor.

```python
from approvedeny import Client

client = Client('your-api-key')
```

### Creating a new check request
To create a new check request, you need to call the `create_check_request` method on the client instance.
```python
check_request = client.create_check_request('check-id', {
  'description': 'A description of the check request',
  'metadata': {
    'key': 'value',
  },
})
```

### Retrieving a check request
To retrieve a check request, you need to call the `get_check_request` method on the client instance.
```python
check_request = client.get_check_request('check-request-id')
```

### Retrieving a check request response
To retrieve a check request response, you need to call the `get_check_request_response` method on the client instance.
```python
check_request_response = client.get_check_request_response('check-request-id')
```

### Verifying webhook signatures
To verify webhook signatures, you need to call the `is_valid_webhook_signature` method on the client instance. This method returns a boolean value indicating whether the signature is valid or not.

```python
is_valid_signature = client.is_valid_webhook_signature('your-encryption-key', 'signature', {'foo': 'bar'})

if is_valid_signature:
  # The signature is valid
else:
  # The signature is invalid
```

### Testing

```bash
pytest
```

### Changelog

Please see [CHANGELOG](CHANGELOG.md) for more information what has changed recently.

## Contributing

Please see [CONTRIBUTING](CONTRIBUTING.md) for details.

### Security

If you discover any security related issues, please use the issue tracker.

## Credits

-   [Olayemi Olatayo](https://github.com/iamolayemi)
-   [Solomon Ajayi](https://github.com/temmyjay001)
-   [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.
