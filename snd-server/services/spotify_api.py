import logging
import anyio
from pydantic import BaseModel
from typing import Callable, TypeVar, Awaitable, TypedDict
from result import Ok, Err, Result
from httpx import Response

from context import Context
from models.error import SoundationsError
from models.spotify import (
    SpotifyApiTrackSearchResponse,
    SpotifyApiTrackSearchResponseTracks,
    SpotifyApiErrorResponse,
)
from models.track import Track, SpotifyTrackSearchResponse, SpotifyTrackFeaturesResponse

logger = logging.getLogger(__name__)


DEFAULT_BACKOFF_SECS = 2
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_URL = "https://api.spotify.com/v1"


TModel = TypeVar("TModel", bound=type(BaseModel))
TOk = TypeVar("TOk")
SpotifyResult = Result[TOk, SoundationsError]


class SpotifyApiCallState(TypedDict):
    retry_attempt: int


default_spotify_api_call_state: SpotifyApiCallState = {"retry_attempt": 1}


class SpotifyApi:
    def __init__(self, ctx: Context):
        self.api = SpotifyApiImpl(ctx)

    async def search_tracks(
        self, q: str, limit: int = 1, offset: int = 0
    ) -> SpotifyResult[SpotifyApiTrackSearchResponseTracks]:
        return await self.api.search_tracks(q=q, limit=limit, offset=offset)

    async def call_spotify_api(
        self,
        call: Callable[[dict[str, str]], Awaitable[Response]],
        model: TModel,
        state: SpotifyApiCallState = default_spotify_api_call_state,
    ) -> SpotifyResult[TModel]:
        return await self.api.call_spotify_api(call=call, model=model, state=state)


class SpotifyApiImpl:
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.access_token: str | None = None

    async def refresh_access_token(self) -> None:
        try:
            response = await self.ctx.http_client.post(
                url=SPOTIFY_TOKEN_URL,
                data={"grant_type": "client_credentials"},
                auth=(
                    self.ctx.config.spotify_client_id,
                    self.ctx.config.spotify_client_secret,
                ),
            )

            response.raise_for_status()

            self.access_token = response.json()["access_token"]

            logger.info("Spotify access token refreshed")
        except Exception as err:
            logger.exception(f"Failed to fetch spotify access token: {str(err)}")

    async def call_spotify_api(
        self,
        call: Callable[[dict[str, str]], Awaitable[Response]],
        model: TModel,
        state: SpotifyApiCallState = default_spotify_api_call_state,
    ) -> SpotifyResult[TModel]:
        if self.access_token is None:
            await self.refresh_access_token()

        headers = {"Authorization": f"Bearer {self.access_token}"}
        try:
            response = await call(headers)
        except Exception as err:
            logger.error(f"Error when calling Spotify API: {str(err)}")
            return Err(SoundationsError(424))

        if not response.is_success:
            retry_attempt = state.get("retry_attempt", 1)

            logger.warning(
                f"HTTP status {response.status_code} when calling Spotify API: {response.text}"
            )

            if response.status_code == 401:
                await self.refresh_access_token()
                return await self.call_spotify_api(call, model)

            if response.status_code in [429, 503]:
                backoff_secs = response.headers.get(
                    "retry-after", DEFAULT_BACKOFF_SECS * retry_attempt
                )
                await anyio.sleep(float(backoff_secs))
                return await self.call_spotify_api(
                    call, model, {"retry_attempt": retry_attempt + 1}
                )

            try:
                error_body = SpotifyApiErrorResponse.parse_raw(response.content)
                error_message = error_body.error.message
            except:
                error_message = None

            return Err(SoundationsError(response.status_code, error_message))

        try:
            return Ok(model.parse_raw(response.content))
        except Exception as err:
            logger.error(f"Error when parsing Spotify API response body: {str(err)}")
            return Err(
                SoundationsError(
                    424, "We received something completely unexpected from Spotify"
                )
            )

    async def search_tracks(
        self,
        q: str,
        limit: int = 1,
        offset: int = 0,
    ) -> SpotifyResult[SpotifyApiTrackSearchResponseTracks]:
        url = f"{SPOTIFY_API_URL}/search?type=track&q={q}&limit={limit}&offset={offset}"

        result = await self.call_spotify_api(
            lambda headers: self.ctx.http_client.get(
                url=url,
                headers=headers,
            ),
            model=SpotifyApiTrackSearchResponse,
        )

        return result.map(lambda resp: resp.tracks)
