#!/bin/sh

curl -s https://raw.githubusercontent.com/Lijs007/SI664-scripts/master/input/un_area_country_codes-m49.csv | \
    tr '\t' ',' > ${PWD}/unsd-m49.csv

