"""This module provides a client for interacting with the Lucidchart API."""

from zipfile import ZipFile

import httpx
import toml

from lucidpy.models import Document
import tempfile


class LucidchartClient:
    """A client for interacting with the Lucidchart API.

    Methods:
        __init__(api_key: str = None):
            Initialize the LucidchartClient with an API key.

        _make_request(method: str, endpoint: str, **kwargs):
            Make an HTTP request to the Lucidchart API.

        search_documents():
            Returns a list of all documents belonging to the requesting user’s account, sorted by created date.

        get_document(document_id: str):
            Retrieve a document by its ID.

        create_document(data: dict):
            Create a new document.
    """

    # update_document(document_id: str, data: dict):
    #     Update an existing document.

    # delete_document(document_id: str):
    #     Delete a document by its ID.

    def __init__(self, api_key: str = None):
        """Initialize the LucidchartClient with an API key.

        Args:
            api_key (str): The API key for authenticating with the Lucidchart API.
        """
        if api_key is None:
            config = toml.load("config.toml")
            api_key = config["api"]["key"]
        self.api_key = api_key
        self.base_url = "https://api.lucid.co"
        self.timeout = httpx.Timeout(30)

    def _make_request(self, method: str, endpoint: str, **kwargs):
        # url
        # headers
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Lucid-Api-Version": "1",
        }
        response = httpx.request(
            method,
            url,
            headers=headers,
            timeout=self.timeout,
            **kwargs,
        )
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()

    def create_document(
        self,
        title: str,
        document: Document = None,
        json: str = "",
    ):
        """Create a new document.

        Args:
            data (dict): The data for the new document.

        Returns:
            dict: The created document data.
        """

        # create a zip file in tmp
        # Create an in-memory bytes buffer

        if document is None and json == "":
            raise ValueError("Either document or json must be provided")
        if document is not None and json != "":
            raise ValueError("Only one of document or json must be provided")

        if document is not None:
            json = document.model_dump_json()

        # Create a zip file in the buffer
        with tempfile.NamedTemporaryFile(delete=False, suffix=".lucid") as tmp_file:
            zip_filename = tmp_file.name
        with ZipFile(zip_filename, "w") as zipf:
            json_filename = "document.json"
            zipf.writestr(json_filename, json)

        # Seek to the beginning of the buffer

        # Prepare the file data for the request
        files = {
            "file": (
                "import.lucid",
                open(zip_filename, mode="rb"),
                "x-application/vnd.lucid.standardImport",
            ),
            "product": (None, "lucidchart"),
            "title": (None, title),
        }

        return self._make_request("POST", "/documents", files=files)

    # def search_documents(self):
    #     """Returns a list of all documents.

    #     Returns all docuemnts belonging to the requesting user’s account, sorted by created date.
    #     """
    #     return self._make_request('POST', endpoint='/documents/search')

    # def get_document(self, document_id: str):
    #     """Retrieve a document by its ID.

    #     Args:
    #         document_id (str): The ID of the document to retrieve.

    #     Returns:
    #         dict: The document data.
    #     """
    #     return self._make_request('GET', f'/documents/{document_id}')

    # def update_document(self, document_id: str, data: dict):
    #     """Update an existing document.

    #     Args:
    #         document_id (str): The ID of the document to update.
    #         data (dict): The data to update the document with.

    #     Returns:
    #         dict: The updated document data.
    #     """
    #     return self._make_request('PUT', f'/documents/{document_id}', json=data)

    # def delete_document(self, document_id: str):
    #     """Delete a document by its ID.

    #     Args:
    #         document_id (str): The ID of the document to delete.

    #     Returns:
    #         dict: The response from the API.
    #     """
    #     return self._make_request('DELETE', f'/documents/{document_id}')
