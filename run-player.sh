#!/usr/bin/env bash

cd "$(dirname "$0")" || exit

if ! command -v python3 > /dev/null 2>&1; then
    echo "Please install python 3 to continue."
    exit
fi

if ! python3 -m pip > /dev/null 2>&1; then
    echo "Please install pip to continue."
    exit
fi

python3 -V

#set -ex

# create new virtual enviornment depending on player name
PLAYER_SUPPLIED=0
for i in "$@"; do
    if [ "$PLAYER_SUPPLIED" -eq "1" ]; then
        VENV_NAME="venv$i"
	break
    fi
    if [ "$i" = "-p" ] || [ "$i" = "--player" ]; then
        PLAYER_SUPPLIED=1
    fi
done

if [ $PLAYER_SUPPLIED -eq "0" ]; then
    echo "Wrong arguments."
    exit 1
fi

# Activate virtual environment
python3 -m venv "$VENV_NAME"
. "$VENV_NAME"/bin/activate

# Install dependencies
python3 -m pip install --upgrade pip setuptools wheel
python3 -m pip install --upgrade -e .

# Run traffic-player
python3 player.py "$@"
