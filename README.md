# Lucidpy
The unofficial Lucid Chart Simple API python wrapper library

This project is a Python library for interacting with the Lucidchart API. It utilizes `httpx` for making HTTP requests and `Pydantic` for data validation and serialization. The library is designed to be flexible and easy to use, allowing developers to integrate Lucidchart functionalities into their applications seamlessly.

## Features

- **API Client**: A robust client for interacting with the Lucidchart API, handling authentication and requests.
- **Data Models**: Pydantic models for validating and serializing API data structures such as documents, pages, and shapes.
- **Utilities**: Helper functions for common tasks related to API interactions.

## Installation

You can install the library using pip:

```
pip install lucidpy
```

## Usage

Here's a basic example of how to use the library:

```python
from lucidpy import LucidchartClient

client = LucidchartClient(api_key='your_api_key')
```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
