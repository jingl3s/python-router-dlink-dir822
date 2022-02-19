# -*- coding: utf-8 -*-
"""
Copyright (C) 2022 Jingl3s

This code is free software; you can redistribute it and/or modify it
under the terms of the DO WHAT THE FUCK YOU WANT TO. (see the file
COPYING.txt included with the distribution).
"""

import functools
import logging
from datetime import datetime
from enum import Enum

from hnap.devices import _LOGGER, Router, auth_required
from hnap.soapclient import MethodCallError, SoapClient


def DeviceDlink822Factory(
    *,
    client=None,
    hostname="dlinkrouter.local",
    password=None,
    username="Admin",
    port=80,
):
    client = client or SoapClient(
        hostname=hostname, password=password, username=username, port=port
    )
    info = client.device_info()
    try:
        # module_device = info["DeviceName"]
        # module_vendor = info["VendorName"]
        module_model = info["ModelName"]
        if "DIR-822" in module_model:
            cls = RouterDlinkDIR822
        else:
            raise TypeError(f"Invalid device as expecte DLINK DIR-822: {info}")
    except KeyError:
        raise TypeError("Invalid device as expecte DLINK DIR-822")

    return cls(client=client)


class RouterDlinkDIR822(Router):
    @auth_required
    def get_wifi_radio_names(self) -> list[str]:
        radios_id = list()
        radio_available = self.client.call("GetOperationMode")
        if "GetOperationModeResult" in radio_available:
            if "OK" == radio_available["GetOperationModeResult"]:
                radios_id = [
                    item["RadioID"] for item in radio_available["OperationModeList"]
                ]
        return radios_id

    @auth_required
    def get_wifi_status(self, radio_name: str) -> bool:
        wifi_enabled = None

        radio_status = self._get_wifi_settings(radio_name)
        if radio_status is not None:
            wifi_enabled = "true" == radio_status["Enabled"]
            _LOGGER.debug(f"Etat Wifi {radio_name}: {wifi_enabled}")

        return wifi_enabled

    @auth_required
    def set_wifi_status(self, radio_name: str, expected_state: bool) -> bool:

        radio_status = self._get_wifi_settings(radio_name)
        if radio_status is not None:
            wifi_enabled = "true" == radio_status["Enabled"]
        else:
            wifi_enabled = None

        if wifi_enabled != expected_state:

            for key_to_delete in ["@xmlns", "GetWLanRadioSettingsResult"]:
                radio_status.pop(key_to_delete, None)
            radio_status["RadioID"] = radio_name
            radio_status["Enabled"] = str(expected_state).lower()
            radio_status["RadioEnabled"] = str(expected_state).lower()

            radio_status_change = self.client.call(
                "SetWLanRadioSettings", **radio_status
            )
            execution_status = False
            if "SetWLanRadioSettingsResult" in radio_status_change:
                execution_status = (
                    "OK" == radio_status_change["SetWLanRadioSettingsResult"]
                )
                wifi_enabled = expected_state

            _LOGGER.info(f"Execution status change etat : {execution_status}")
        return wifi_enabled

    @auth_required
    def get_interface_stats(self, interface: str):
        stat_interface = self.client.call("GetInterfaceStatistics", Interface=interface)
        _LOGGER.debug(f"get_interface_stats : {stat_interface}")
        return stat_interface

    @auth_required
    def _get_wifi_settings(self, radio_name: str) -> bool:
        radio_status = self.client.call("GetWLanRadioSettings", RadioID=radio_name)
        if "GetWLanRadioSettingsResult" in radio_status:
            if "OK" == radio_status["GetWLanRadioSettingsResult"]:
                return radio_status

        return None
