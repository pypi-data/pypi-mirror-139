"""Fox dimmable device implementation."""

import json

from foxrestapiclient.connection import _LOGGER
from foxrestapiclient.connection.const import (API_RESPONSE_STATUS_FAIL,
                                               API_RESPONSE_STATUS_INVALID,
                                               REQUEST_CHANNEL_KEY)
from foxrestapiclient.connection.rest_api_client import RestApiClient
from foxrestapiclient.connection.rest_api_responses import (
    RestApiBaseResponse, RestApiBrightnessResponse)

from .const import API_DIMMABLE_GET_BRIGHTNESS, API_DIMMABLE_SET_BRIGHTNESS
from .fox_base_device import DeviceData, FoxBaseDevice


class FoxDimmableDevice(FoxBaseDevice):
    """Fox Dimmable device implementation. Base class for any device with dimmable feature."""

    def __init__(self, device_data: DeviceData):
        """Initialize object."""
        super().__init__(device_data)
        #Extened RestApi methods, specific for device
        self.__device_api_client = self.DeviceRestApiImplementer(self._rest_api_client)

    class DeviceRestApiImplementer:
        """Inner class with specific RestApi methods definition used by device."""

        def __init__(self, rest_api_client: RestApiClient) -> None:
            """Initialize object."""
            self._rest_api_client = rest_api_client

        async def async_get_brightness_value(self, params) -> RestApiBrightnessResponse:
            """Get brightness value by given channel.

            Keyword arguments:
            params -- params dictionary, should contain channel number
            Return:
            RestApiBrightnessResponse
            """
            device_response = await self._rest_api_client.async_make_api_call_get(
                API_DIMMABLE_GET_BRIGHTNESS, params)
            if device_response is None:
                return RestApiBrightnessResponse(status=API_RESPONSE_STATUS_FAIL)
            return RestApiBrightnessResponse(**json.loads(device_response))

        async def async_set_brighntess_value(self, params) -> RestApiBaseResponse:
            """Set brightness value.

            Keyword arguments:
            params -- params dictionary, should contain channel number
            Return:
            RestApiBaseResponse
            """
            device_response = await self._rest_api_client.async_make_api_call_get(
                API_DIMMABLE_SET_BRIGHTNESS, params)
            if device_response is None:
                return RestApiBaseResponse(API_RESPONSE_STATUS_FAIL)
            return RestApiBaseResponse(**json.loads(device_response))

    async def async_fetch_channel_brightness(self, channel: int = 0) -> list:
        """Fetch device brightness value by given channel.

        If channel number not provided fetch brightness from all channels.

        Keyword arguments:
        channel -- channel number
        Return:
        list(int) -- readed values.
        """
        params = None
        if channel != 0:
            params = {
                REQUEST_CHANNEL_KEY: str(channel)
            }
        device_response = await self.__device_api_client.async_get_brightness_value(params)
        if device_response.status in (API_RESPONSE_STATUS_FAIL, API_RESPONSE_STATUS_INVALID):
            return [0,0]
        values = []
        if device_response.brightness != -1:
            values.append(device_response.brightness)
        if device_response.channel_1_value != -1:
            values.append(device_response.channel_1_value)
        if device_response.channel_2_value != -1:
            values.append(device_response.channel_2_value)
        return values

    async def async_update_channel_brightness(self, brightness: int, channel: int = None) -> bool:
        """Set brightness value on device.

        Keyword arguments:
        brightness -- value from range <0-255>
        channel -- value from range <1-2> or None.
        """
        if brightness < 0 or brightness > 255:
            _LOGGER.warning(
                "Brightness passed to sync_update_channel_brightness() is out of range.")
            return False
        if channel is not None and (channel < 0 or channel > 2):
            _LOGGER.warning(
                "Channel passed to sync_update_channel_brightness() is out of range.")
            return False
        params = {
            "value": brightness
        }
        if channel is not None:
            params.update({REQUEST_CHANNEL_KEY: channel})
        device_response = await self.__device_api_client.async_set_brighntess_value(params)
        if device_response.status in (API_RESPONSE_STATUS_FAIL, API_RESPONSE_STATUS_INVALID):
            _LOGGER.error("Setting brightness value in async_update_channel_brightness() failed.")
        return True

