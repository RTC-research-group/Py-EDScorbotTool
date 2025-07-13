#!/bin/bash

f="${1%.*}_refs.npy"
python3.8 angles_to_refs.py $1 -o $f

python3.8 pad_trajectory.py $f -o ${1%.*}_refs_6dims.json