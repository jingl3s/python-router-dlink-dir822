# Python clients for Dlink DIR-822 HNAP device

Based on work of project https://github.com/ldotlopez/python-hnap

HNAP client used with Dlink DIR-822
This could probably work with other devices

## Objective

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



**Useful links**

  * [Product page](https://eu.dlink.com/es/es/products/dch-s220-mydlink-home-siren)
  * [REST API in NodeJS](https://github.com/mtflud/DCH-S220-Web-Control)
  * https://github.com/waffelheld/dlink-device-tracker
  * https://github.com/bikerp/dsp-w215-hnap
  * https://github.com/postlund/dlink_hnap
