"""Tests for API client."""

from unittest.mock import Mock
from pln_search.api import PLNAPIClient


def test_client_initialization():
    """Test API client can be initialized."""
    mock_auth = Mock()
    mock_auth.get_valid_token.return_value = "test_token"

    client = PLNAPIClient(
        base_url="https://api.test.com",
        auth=mock_auth
    )

    assert client.base_url == "https://api.test.com"
    assert client.auth == mock_auth
