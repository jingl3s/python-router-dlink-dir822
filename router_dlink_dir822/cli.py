# -*- coding: utf-8 -*-
#
"""
Copyright (C) 2022 Jingl3s

This code is free software; you can redistribute it and/or modify it
under the terms of the DO WHAT THE FUCK YOU WANT TO. (see the file
COPYING.txt included with the distribution).
"""


import argparse
import logging
import os
import pprint
import sys
import xml.dom.minidom

import requests

import device_dlink_dir822

OUTPUT_TMPL = """
Device info
===========
{info}

Device actions
==============
{device_actions}

SOAP actions
==============
{soap_actions}
"""


def main():
    logging.basicConfig()
    logger = logging.getLogger("router_dlink_dir822")
    logger.setLevel(logging.DEBUG)
    

    parser = argparse.ArgumentParser()
    # parser.add_argument("--hostname", required=True)
    parser.add_argument(
        "--password",
        default=os.environ.get("HNAP_PASSWORD", ""),
        required=False,
    )

    subparser = parser.add_subparsers(dest="command")
    net_stat = subparser.add_parser("net-stat")
    wifi = subparser.add_parser("wifi")
    # wifi_params = wifi.add_subparsers(dest="wifi")

    wifi.add_argument("-c", "--change-state", default=None, type=int)
    wifi.add_argument("-s", "--state", action='store_true')
    wifi.add_argument("-r", "--radio-name", default="RADIO_2.4GHz", type=str)
    net_stat.add_argument("-w", "--wifi-name", default="WLAN2.4G", type=str)
    args = parser.parse_args()

    try:

        if "wifi" == args.command:
            dlink_router = device_dlink_dir822.DeviceDlink822Factory(
                password=args.password
            )

            if args.change_state is not None:
                # text_commande = "Wifi: " + args.change_state
                expected_state = not (0 == args.change_state)
                dlink_router.set_wifi_status(args.radio_name, args.change_state)
                return 0

            elif args.state:
                value = dlink_router.get_wifi_status(args.radio_name)
                if True == value:
                    return 0
                return 1
            else:
                print("Missing optional parameter")
                parser.print_help()
                return 20

        elif "net-stat" == args.command:
            logger.setLevel(logging.WARN)
            dlink_router = device_dlink_dir822.DeviceDlink822Factory(
                password=args.password
            )

            # text_commande = "Retrieve stats"
            stat = dlink_router.get_interface_stats(args.wifi_name)
            json_out = json.dumps(stat, indent=4, sort_keys=True)
            # pprint.pprint(stat)
            print(json_out)
            return 0

        else:
            print(
                OUTPUT_TMPL.format(
                    info=pprint.pformat(client.device_info()),
                    soap_actions=pprint.pformat(client.soap_actions()),
                    device_actions=pprint.pformat(client.device_actions()),
                ).strip()
            )
            parser.print_help()

    except Exception as e:
        print(f"Exception {e}")
        return 10


if __name__ == "__main__":
    sys.exit(main())
