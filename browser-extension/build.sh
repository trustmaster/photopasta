#!/bin/sh
# This script is run before loading/packaging browser extensions.
# It is a workaround for different browser requirements while avoiding
# duplicate source files.

cp -Rp images chrome/
cp -Rp src chrome/
cp -Rp images firefox/
cp -Rp src firefox/
