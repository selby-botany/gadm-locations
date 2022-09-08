#!/bin/bash

for c in $(cat ${PWD}/countries.csv | cut -d, -f1); do
    echo -n "${c} ..."
    for n in $(seq 10 -1 1); do
        url="https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_${c}_${n}.json"
        echo "trying ${url}"
        if (($(curl --silent -I "${url}" | grep -E "^HTTP" | awk -F " " '{print $2}') == 200)); then
            echo "downloading ${url}" 
            curl -s -k "${url}" > "${PWD}/data/gadm41_${c}_${n}.json"
            break
	else
            echo "File not found: ${url}"
        fi
    done
    echo
done

