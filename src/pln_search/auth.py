"""OAuth2 authentication flow."""

import requests
from datetime import datetime
from pln_search.config import ConfigManager


class AuthenticationError(Exception):
    """Authentication failed."""
    pass


class OAuth2Flow:
    """Handle OAuth2 authentication flow."""

    def __init__(self, api_base_url: str, config: ConfigManager):
        """Initialize OAuth2 flow.

        Args:
            api_base_url: Base URL for API
            config: Configuration manager
        """
        self.api_base_url = api_base_url.rstrip("/")
        self.config = config

    def get_valid_token(self) -> str:
        """Get a valid access token, refreshing if needed.

        Returns:
            Valid access token

        Raises:
            AuthenticationError: If not authenticated or refresh fails
        """
        creds = self.config.load_credentials()

        if not creds:
            raise AuthenticationError(
                "Not authenticated. Run: pln-search auth"
            )

        # Check if token is expired
        expires_at = datetime.fromisoformat(creds["expires_at"])
        now = datetime.now()

        # Refresh if expired or expiring soon (< 5 minutes)
        if expires_at <= now or (expires_at - now).total_seconds() < 300:
            return self._refresh_token(creds["refresh_token"])

        return creds["access_token"]

    def _refresh_token(self, refresh_token: str) -> str:
        """Refresh access token using refresh token.

        Args:
            refresh_token: Refresh token

        Returns:
            New access token

        Raises:
            AuthenticationError: If refresh fails
        """
        url = f"{self.api_base_url}/v1/auth/token"

        try:
            response = requests.post(
                url,
                json={
                    "grantType": "refresh_token",
                    "refreshToken": refresh_token,
                },
                timeout=30,
            )

            response.raise_for_status()
            data = response.json()

            # Update stored credentials
            self.config.save_credentials({
                "access_token": data["accessToken"],
                "refresh_token": data["refreshToken"],
                "expires_at": datetime.now().isoformat(),  # TODO: Calculate from expires_in
                "user_info": data.get("userInfo", {}),
            })

            return data["accessToken"]

        except requests.exceptions.RequestException as e:
            raise AuthenticationError(f"Token refresh failed: {e}")

    def start_auth_flow(self) -> None:
        """Start OAuth2 browser authentication flow.

        This will:
        1. Create auth request
        2. Open browser to consent page
        3. Start localhost server
        4. Exchange code for tokens
        5. Save credentials
        """
        # TODO: Implement full OAuth2 flow
        # For now, print instructions
        print("OAuth2 browser flow not yet implemented.")
        print("Manual token entry:")
        print("1. Obtain access token from PLN API")
        print("2. Save to credentials manually")
        raise NotImplementedError("Full OAuth2 flow coming soon")
