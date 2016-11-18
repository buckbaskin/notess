#!/bin/bash

echo Stopping server ...
kill $(pgrep -f start.sh)
