#!/bin/bash
cd "`dirname $0`"
pip3 install -r requirements.txt
python3 runserver.py > /dev/null 2>&1 &
