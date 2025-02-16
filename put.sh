#! /bin/bash

circuitpy="/Volumes/CIRCUITPY"
ex="examples"

# Check if the CIRCUITPY drive is mounted
if [ ! -d "${circuitpy}" ]; then
    echo "CIRCUITPY drive is not mounted."
    exit 1
fi

# Make sure we have a name in the first argument
if [ -z "$1" ]; then
    echo "Usage: $0 <name>"
    exit 1
fi

# Make sure the name exists
if [ ! -f "${ex}/$1" ]; then
    echo "File ${ex}/$1 does not exist."
    exit 1
fi

# copy named file to CIRCUITPY/code.py
cp "${ex}/$1" "${circuitpy}/code.py"

echo "Copied ${ex}/$1 to code.py on CIRCUITPY drive."