# -*- coding: utf-8 -*-
#
"""
Copyright (C) 2022 Jingl3s

This code is free software; you can redistribute it and/or modify it
under the terms of the DO WHAT THE FUCK YOU WANT TO. (see the file
COPYING.txt included with the distribution).
"""

import argparse
import json
import logging
import os
import sys

import device_dlink_dir822


def main():
    logging.basicConfig()
    logger = logging.getLogger("router_dlink_dir822")
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--password",
        default=os.environ.get("HNAP_PASSWORD", ""),
        required=False,
    )

    subparser = parser.add_subparsers(dest="command")
    statistic = subparser.add_parser("statistic")
    wifi = subparser.add_parser("wifi")
    # wifi_params = wifi.add_subparsers(dest="wifi")

    wifi.add_argument("-c", "--change-state", default=None, type=int)
    wifi.add_argument("-s", "--state", action="store_true")
    wifi.add_argument("-r", "--radio-name", default="RADIO_2.4GHz", type=str)
    statistic.add_argument("-w", "--wifi-name", default="WLAN2.4G", type=str)
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

        elif "statistic" == args.command:
            logger.setLevel(logging.WARN)
            dlink_router = device_dlink_dir822.DeviceDlink822Factory(
                password=args.password
            )

            # text_commande = "Retrieve stats"
            stat = dlink_router.get_interface_stats(args.wifi_name)
            json_out = json.dumps(stat, indent=4, sort_keys=True)
            print(json_out)
            return 0
        else:
            print("Missing parameter")
            parser.print_help()
            return 20

    except Exception as e:
        print(f"Exception {e}")
        return 10


if __name__ == "__main__":
    sys.exit(main())
