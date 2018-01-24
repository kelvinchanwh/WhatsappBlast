#!/bin/sh
dir=${0%/*}
if [ "$dir" = "$0" ]; then
  dir="."
fi
cd "$dir"

python WhatsappBlast.py