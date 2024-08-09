#!/bin/bash

find /tmp -maxdepth 1 -cmin +60 -type d -regex ".*rust_.*\|.*Temp-.*\|.*pymp.*\|.*config-util.*-cache" -exec rm -r {} \;

