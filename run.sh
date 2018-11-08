#!/bin/bash

cd $(dirname $0)

if ! which yarn > /dev/null 2>&1; then
    echo "Please install yarn to continue."
    exit
fi

if ! which yarn > /dev/null 2>&1; then
    echo "Please install python3 to continue."
    exit
elif [[ $(python3 -V 2>&1) == *"Python 3.6"* ]] || [[ $(python3 -V 2>&1) == *"Python 3.7"* ]]; then
    python3 -V
else
    echo "Please install Python 3.6+ to continue."
    exit
fi

if ! python3 -m pip > /dev/null 2>&1; then
    echo "Please install pip to continue."
    exit
fi

set -ex

# Building web-frontend...
cd frontend
yarn install
yarn build
cd ..

python3 -m venv venv
. venv/bin/activate

python3 -m pip install --upgrade -e .

python3 app.py
