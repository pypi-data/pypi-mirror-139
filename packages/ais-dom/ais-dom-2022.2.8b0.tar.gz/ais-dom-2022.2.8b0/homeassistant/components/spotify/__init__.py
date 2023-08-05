"""The spotify integration."""
from __future__ import annotations

from datetime import timedelta
from typing import Any

import aiohttp
import requests
from spotipy import Spotify, SpotifyException
import voluptuous as vol

from homeassistant.components.media_player import BrowseError
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    ATTR_CREDENTIALS,
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    Platform,
)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed, ConfigEntryNotReady
from homeassistant.helpers import config_entry_oauth2_flow, config_validation as cv
from homeassistant.helpers.config_entry_oauth2_flow import (
    OAuth2Session,
    async_get_config_entry_implementation,
)
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from . import config_flow
from .const import (
    DATA_SPOTIFY_CLIENT,
    DATA_SPOTIFY_DEVICES,
    DATA_SPOTIFY_ME,
    DATA_SPOTIFY_SESSION,
    DOMAIN,
    LOGGER,
    MEDIA_PLAYER_PREFIX,
    SPOTIFY_SCOPES,
)
from .media_player import async_browse_media_internal

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Inclusive(CONF_CLIENT_ID, ATTR_CREDENTIALS): cv.string,
                vol.Inclusive(CONF_CLIENT_SECRET, ATTR_CREDENTIALS): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)

PLATFORMS = [Platform.MEDIA_PLAYER]


def is_spotify_media_type(media_content_type):
    """Return whether the media_content_type is a valid Spotify media_id."""
    return media_content_type.startswith(MEDIA_PLAYER_PREFIX)


def resolve_spotify_media_type(media_content_type):
    """Return actual spotify media_content_type."""
    return media_content_type[len(MEDIA_PLAYER_PREFIX) :]


async def async_browse_media(
    hass, media_content_type, media_content_id, *, can_play_artist=True
):
    """Browse Spotify media."""
    if not (info := next(iter(hass.data[DOMAIN].values()), None)):
        raise BrowseError("No Spotify accounts available")
    return await async_browse_media_internal(
        hass,
        info[DATA_SPOTIFY_CLIENT],
        info[DATA_SPOTIFY_SESSION],
        info[DATA_SPOTIFY_ME],
        media_content_type,
        media_content_id,
        can_play_artist=can_play_artist,
    )


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Spotify integration."""
    if DOMAIN not in config:
        return True

    if CONF_CLIENT_ID in config[DOMAIN]:
        config_flow.SpotifyFlowHandler.async_register_implementation(
            hass,
            config_entry_oauth2_flow.LocalOAuth2Implementation(
                hass,
                DOMAIN,
                config[DOMAIN][CONF_CLIENT_ID],
                config[DOMAIN][CONF_CLIENT_SECRET],
                "https://accounts.spotify.com/authorize",
                "https://accounts.spotify.com/api/token",
            ),
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Spotify from a config entry."""
    implementation = await async_get_config_entry_implementation(hass, entry)
    session = OAuth2Session(hass, entry, implementation)

    try:
        await session.async_ensure_token_valid()
    except aiohttp.ClientError as err:
        raise ConfigEntryNotReady from err

    spotify = Spotify(auth=session.token["access_token"])

    try:
        current_user = await hass.async_add_executor_job(spotify.me)
    except SpotifyException as err:
        raise ConfigEntryNotReady from err

    async def _update_devices() -> list[dict[str, Any]]:
        if not session.valid_token:
            await session.async_ensure_token_valid()
            await hass.async_add_executor_job(
                spotify.set_auth, session.token["access_token"]
            )

        try:
            devices: dict[str, Any] | None = await hass.async_add_executor_job(
                spotify.devices
            )
        except (requests.RequestException, SpotifyException) as err:
            raise UpdateFailed from err

        if devices is None:
            return []

        return devices.get("devices", [])

    device_coordinator: DataUpdateCoordinator[
        list[dict[str, Any]]
    ] = DataUpdateCoordinator(
        hass,
        LOGGER,
        name=f"{entry.title} Devices",
        update_interval=timedelta(minutes=5),
        update_method=_update_devices,
    )
    await device_coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_SPOTIFY_CLIENT: spotify,
        DATA_SPOTIFY_DEVICES: device_coordinator,
        DATA_SPOTIFY_ME: current_user,
        DATA_SPOTIFY_SESSION: session,
    }

    if not set(session.token["scope"].split(" ")).issuperset(SPOTIFY_SCOPES):
        raise ConfigEntryAuthFailed

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Spotify config entry."""
    # Unload entities for this entry/device.
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    # Cleanup
    del hass.data[DOMAIN][entry.entry_id]
    if not hass.data[DOMAIN]:
        del hass.data[DOMAIN]

    return unload_ok
