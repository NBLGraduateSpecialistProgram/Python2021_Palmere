#!/usr/bin/env bash

echo "Unintalling matrix module..."
python3 -m pip uninstall matrix
rm -r build/
rm -r dist/
rm -r matrix.egg-info/
