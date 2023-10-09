#/usr/bin/bash

lCheminTravail=$(cd `dirname $0` && pwd) >/dev/null
cd $lCheminTravail/..
python3 -m venv venv
venv/bin/python3 -m pip install -r requirements.txt
cd - > /dev/null
if [ ! -z $lCheminTravail/launch_shell.sh ];then
cp $lCheminTravail/launch_shell.sh.sample $lCheminTravail/launch_shell.sh
fi