#!/bin/bash
set -evx

mkdir ~/.helpcore

# safety check
if [ ! -f ~/.helpcore/.help.conf ]; then
  cp share/help.conf.example ~/.helpcore/help.conf
fi
