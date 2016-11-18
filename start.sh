#!/bin/bash

echo Running Mongo script ....
./run_mongo.sh &

sleep 3

echo Starting app server ....
python3 run.py
