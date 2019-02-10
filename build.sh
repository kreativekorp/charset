#!/usr/bin/env bash
set -e
rm -rf out
cp -Rf src out

echo Downloading Unicode data...
python bin/list-unidata.py

echo Downloading fonts...
python bin/list-fonts.py

python bin/build-public.py
python bin/build-ucd-js.py
python bin/build-unicode.py
python bin/build-encoding.py
