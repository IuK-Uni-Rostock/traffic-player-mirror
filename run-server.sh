#!/usr/bin/env bash

cd "$(dirname "$0")" || exit

if ! command -v yarn > /dev/null 2>&1; then
    echo "Please install yarn to continue."
    exit
fi

if ! command -v python3 > /dev/null 2>&1; then
    echo "Please install python 3 to continue."
    exit
else
    # Check python version
    version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
    parsedVersion="${version//./}"
    if [ "$parsedVersion" -lt "360" ]; then
       echo "Please install python 3.6+ to continue."
       exit
    fi
fi

if ! python3 -m pip > /dev/null 2>&1; then
    echo "Please install pip to continue."
    exit
fi

python3 -V

#set -ex

# Build web-frontend
cd frontend
yarn install
yarn build
cd ..

# Activate virtual environment
python3 -m venv venv
. venv/bin/activate

# Install dependencies
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install --upgrade -e .

# Run traffic-player server
python3 server.py
