"""Inels switch entity."""
from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from inelsmqtt.devices import Device

from inelsmqtt.const import (
    # Inels types
    RFSC_61,
    SA3_01B,
    DA3_22M,
    GTR3_50,
    GSB3_90SX,
)

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .base_class import InelsBaseEntity
from .const import DEVICES, DOMAIN, ICON_SWITCH, LOGGER


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Load Inels switch.."""
    device_list = hass.data[DOMAIN][config_entry.entry_id][DEVICES]

    entities = []
    for device in device_list:
        if device.device_type == Platform.SWITCH:
            if device.inels_type == RFSC_61:
                entities.append(InelsSwitch(device=device))
            elif device.inels_type == SA3_01B:
                entities.append(InelsSwitch(device=device))
                # LOGGER.info("Added SA3_01B (%s)", device.get_unique_id())

    async_add_entities(entities, True)


class InelsSwitch(InelsBaseEntity, SwitchEntity):
    """The platform class required by Home Assistant."""

    def __init__(self, device: Device) -> None:
        """Initialize a switch."""
        super().__init__(device=device)

        self._is_on = False  # TODO get a more permanent solution

        # self._state_attrs = None

        # if isinstance(device.state, bool) is False:
        #     if hasattr(device.state, "on"):
        #         self._state_attrs = {
        #             ATTR_TEMPERATURE: device.state.temperature,
        #             "on": device.state.on,
        #         }

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        # if isinstance(self._device.state, bool) is False:
        #     if hasattr(self._device.state, "on"):
        #         return self._device.state.on

        return self._is_on

        # ha_val = self._device.get_value().ha_value
        # return ha_val == True

    @property
    def icon(self) -> str | None:
        """Switch icon."""
        return ICON_SWITCH

    # @property
    # def extra_state_attributes(self) -> Mapping[str, Any] | None:
    #     """Extra attributes if exists."""
    #     if self._state_attrs is None:
    #         return super().extra_state_attributes
    #     return self._state_attrs

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the switch to turn off."""
        if not self._device.is_available:
            return None

        await self.hass.async_add_executor_job(self._device.set_ha_value, False)
        self._is_on = False

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the switch to turn on."""
        if not self._device.is_available:
            return None

        await self.hass.async_add_executor_job(self._device.set_ha_value, True)
        self._is_on = True

    def _callback(self, new_value: Any) -> None:
        """Get callback data from the broker."""
        super()._callback(new_value)
        # if self._state_attrs is not None:
        #     if isinstance(self._device.state, bool) is False:
        #         self._state_attrs[ATTR_TEMPERATURE] = self._device.state.temperature
        #         self._state_attrs["on"] = self._device.state.on


class InelsComplexSwitch(InelsBaseEntity, SwitchEntity):
    """The platform class required by Home Assistant."""

    def __init__(self, device: Device) -> None:
        """Initialize a switch."""
        super().__init__(device=device)

        # self._state_attrs = None

        # if isinstance(device.state, bool) is False:
        #     if hasattr(device.state, "on"):
        #         self._state_attrs = {
        #             ATTR_TEMPERATURE: device.state.temperature,
        #             "on": device.state.on,
        #         }

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        # if isinstance(self._device.state, bool) is False:
        #     if hasattr(self._device.state, "on"):
        #         return self._device.state.on

        return self._device.state

    @property
    def icon(self) -> str | None:
        """Switch icon."""
        return ICON_SWITCH

    # @property
    # def extra_state_attributes(self) -> Mapping[str, Any] | None:
    #     """Extra attributes if exists."""
    #     if self._state_attrs is None:
    #         return super().extra_state_attributes
    #     return self._state_attrs

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Instruct the switch to turn off."""
        if not self._device.is_available:
            return None

        ha_val = self._device.get_value().ha_value
        ha_val.on = False
        await self.hass.async_add_executor_job(self._device.set_ha_value, ha_val)

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Instruct the switch to turn on."""
        if not self._device.is_available:
            return None

        ha_val = self._device.get_value().ha_value
        ha_val.on = True
        await self.hass.async_add_executor_job(self._device.set_ha_value, ha_val)

    def _callback(self, new_value: Any) -> None:
        """Get callback data from the broker."""
        super()._callback(new_value)
        # if self._state_attrs is not None:
        #     if isinstance(self._device.state, bool) is False:
        #         self._state_attrs[ATTR_TEMPERATURE] = self._device.state.temperature
        #         self._state_attrs["on"] = self._device.state.on
