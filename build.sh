#!/usr/bin/env bash
set -e
rm -rf out
cp -Rf src out

echo Downloading Unicode data...
python2 bin/list-unidata.py

echo Downloading fonts...
python2 bin/list-fonts.py

python2 bin/build-public.py
python2 bin/build-ucd-js.py
python2 bin/build-unicode.py
python2 bin/build-encoding.py

export COPYFILE_DISABLE=true
find out -name .DS_Store -delete
tar -zcvf charset.tgz out
