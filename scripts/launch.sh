#/usr/bin/bash

lCheminTravail=$(cd `dirname $0` && pwd) >/dev/null
cmd_python="${lCheminTravail}/../venv/bin/python3"
$cmd_python $lCheminTravail/../router_dlink_dir822/cli.py $*
