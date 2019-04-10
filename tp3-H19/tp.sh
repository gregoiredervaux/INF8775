#!/bin/bash

OPTIONS=""
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -e)
    EX_PATH="$2"
    ;;
    *)
        echo "Argument inconnu: ${1}"
        exit
    ;;
esac
shift
done

python3 ./src/Algo.py $EX_PATH $OPTIONS
