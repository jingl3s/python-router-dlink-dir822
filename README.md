# Python clients for Dlink DIR-822 HNAP device

Based on work of project https://github.com/ldotlopez/python-hnap

HNAP client used with Dlink DIR-822
This could probably work with other devices

## Objectives

This project is derivated to be only dedicated to Router DLINK DIR-822 with my own usage

* Not expected to be published under Pypi
* Not expected to put in place more settings

## Setup

### Requirement

Python 3.x

### Installation

```shell
git clone https://github.com/jingl3s/python-router-dlink_dir822
cd python-router-dlink_dir822
python3 -m venv venv
pip3 install -r requirements.txt
```

### Usage

Environment variable for password or as command line
HNAP_PASSWORD or --password

* Enable the wifi
`router_dlink_dir822 wifi -c 1`

* Get the wifi state by using the name of the Wifi
`router_dlink_dir822 wifi -c 1 -r RADIO_2.4GHz`

* Get the network statistic with the name of component
`router_dlink_dir822 statistic -w WLAN2.4G`

### Build

```shell
python3 -m pip install --upgrade build
python3 -m build
```

## How to retrieve some extra information

### How to get calls used here

* Use of browser in developer mode
* In network, filter HNAP
* Go through the POST request to retrieve the calls of a dedicated page content you need
* Retrieve that and adapt inside the source code

### How to get the different interface for network stats

* Follow previous step by going into section of statistics
* Retrieve the last 

### Sample development

```python
import hnap
import secret
import logging
import device_dlink_dir822

client = hnap.soapclient.SoapClient(
    "dlinkrouter.local", password=secret.pass_word, username="Admin"
)
logging.basicConfig()
logger = logging.getLogger("hnap")
logger.setLevel(logging.DEBUG)
client.authenticate()
print(client.authenticated)
print(repr(client.call("GetDeviceSettings")))
print(repr(client.call("GetWLanRadios")))
logger.debug(f"device_info: {client.device_info()}")
logger.debug(f"device_actions: {client.device_actions()}")


dlink_router = router_dlink_dir822.device_dlink_dir822.DeviceDlink822Factory(password=secret.pass_word)
radios_id = dlink_router.get_wifi_radio_names()
print(radio_id)
```

**Useful links**

* Base project https://github.com/ldotlopez/python-hnap
* [Product page](https://eu.dlink.com/es/es/products/dch-s220-mydlink-home-siren)
* [REST API in NodeJS](https://github.com/mtflud/DCH-S220-Web-Control)
* https://github.com/waffelheld/dlink-device-tracker
* https://github.com/bikerp/dsp-w215-hnap
* https://github.com/postlund/dlink_hnap
* https://github.com/ayavilevich/homeassistant-dlink-presence/blob/master/custom_components/dlink_presence/dlink_telnet.py
* https://github.com/jakekara/jnap
* https://github.com/fwupd/fwupd
