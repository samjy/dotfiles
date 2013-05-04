#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Loaded when launching interpreter.

Don't forget to specify it in PYTHONSTARTUP environment variable.
"""

import os
import readline
import atexit
import rlcompleter

# history file, load history
history_file = os.path.expanduser('~/.python_history')
readline.read_history_file(history_file)

# save history when exiting
atexit.register(readline.write_history_file, history_file)

# set autocompletion
readline.parse_and_bind('tab: complete')

#EOF
