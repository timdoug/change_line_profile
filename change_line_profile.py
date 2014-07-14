#!/usr/bin/env python
#
# change_line_profie.py - a tool to change Sonic.net Annex A/M line profiles
# Copyright (c) 2014, timdoug
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import ConfigParser
import os
import sys

import requests

if len(sys.argv) != 2:
    sys.exit('usage: %s upload|download' % sys.argv[0])

desired_profile = sys.argv[1]
if desired_profile not in ('upload', 'download'):
    sys.exit('Only valid profiles are upload and download.')

config_parser = ConfigParser.ConfigParser()
config_parser.read(os.path.expanduser('~/.sonicnet'))

try:
    config = dict(config_parser.items('fusion'))
    user, password, number = config['user'], config['password'], config['number']
except (ConfigParser.NoSectionError, KeyError):
    sys.exit('Error reading config file!')

s = requests.Session()
print 'Authenticating...',
# This GET is necessary to retrieve a PHPSESSID cookie before authenticating;
# without it, the subsequent POST with credentials doesn't work.
s.get('https://members.sonic.net/')
s.post('https://members.sonic.net/', data={'login': 'login', 'user': user, 'pw': password})
print 'done.'

run_profile_command = lambda cmd: s.post('https://members.sonic.net/fusion-line-profile/',
    data={'action': cmd, 'FusionTn': number})

res = run_profile_command('ToggleFusionTn')
current_profile = res.json()['fusion_this_mode'].lower()
if current_profile == desired_profile:
    sys.exit('Current profile is already %s.' % current_profile)

print 'Changing profile to %s...' % desired_profile,
run_profile_command('SetFusionMode')
print 'done.'
