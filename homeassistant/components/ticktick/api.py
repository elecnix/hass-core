"""API for TickTick bound to Home Assistant OAuth."""

from aiohttp import ClientResponse, ClientSession

from homeassistant.helpers import config_entry_oauth2_flow

# the following two API examples are based on our suggested best practices
# for libraries using OAuth2 with requests or aiohttp. Delete the one you won't use.
# For more info see the docs at https://developers.home-assistant.io/docs/api_lib_auth/#oauth2.


# class ConfigEntryAuth(my_pypi_package.AbstractAuth):
# class ConfigEntryAuth:
#     """Provide TickTick authentication tied to an OAuth2 based config entry."""

#     def __init__(
#         self,
#         hass: HomeAssistant,
#         oauth_session: config_entry_oauth2_flow.OAuth2Session,
#     ) -> None:
#         """Initialize TickTick Auth."""
#         self.hass = hass
#         self.session = oauth_session
#         # super().__init__(self.session.token)

#     def refresh_tokens(self) -> str:
#         """Refresh and return new TickTick tokens using Home Assistant OAuth2 session."""
#         run_coroutine_threadsafe(
#             self.session.async_ensure_token_valid(), self.hass.loop
#         ).result()

#         return self.session.token["access_token"]


class AbstractAuth:
    """Abstract class to make authenticated requests."""

    def __init__(self, websession: ClientSession) -> None:
        """Initialize the auth."""
        self.websession = websession
        self.host = "thehost"

    async def async_get_access_token(self) -> str:
        """Doc."""
        return """Return a valid access token."""

    async def request(self, method, url, **kwargs) -> ClientResponse:
        """Make a request."""
        headers = kwargs.get("headers")

        if headers is None:
            headers = {}
        else:
            headers = dict(headers)

        access_token = await self.async_get_access_token()
        headers["authorization"] = f"Bearer {access_token}"

        return await self.websession.request(
            method,
            f"{self.host}/{url}",
            **kwargs,
            headers=headers,
        )


class AsyncConfigEntryAuth(AbstractAuth):
    """Provide TickTick authentication tied to an OAuth2 based config entry."""

    def __init__(
        self,
        websession: ClientSession,
        oauth_session: config_entry_oauth2_flow.OAuth2Session,
    ) -> None:
        """Initialize TickTick auth."""
        super().__init__(websession)
        self._oauth_session = oauth_session

    async def async_get_access_token(self) -> str:
        """Return a valid access token."""
        if not self._oauth_session.valid_token:
            await self._oauth_session.async_ensure_token_valid()

        return self._oauth_session.token["access_token"]
