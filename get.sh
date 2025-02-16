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

# if we already have a file by this name, move it to a backup
if [ -f "${ex}/$1" ]; then
    mv "${ex}/$1" "${ex}/${1}.bak"
    echo "Moved existing file $1 to ${1}.bak"
fi

# copy code.py from CIRCUITPY to the current directory
# under the name given in the first argument
cp "${circuitpy}/code.py" "${ex}/$1"

echo "Copied code.py to ${ex}/$1"