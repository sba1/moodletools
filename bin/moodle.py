#!/usr/bin/env python3

import argcomplete # type: ignore
import argparse
import logging
import glob
import os
import requests
import re
import subprocess
import sys
import xdg # type: ignore

from lxml import html # type: ignore

from typing import Set

DEBUG = False

script = os.path.realpath(sys.argv[0])
scriptdir = os.path.realpath(os.path.dirname(script))
progname = os.path.basename(sys.argv[0])
prefix = 'moodle-'

commands = glob.glob(os.path.join(scriptdir,"{0}*".format(prefix)))
commands = [os.path.basename(command) for command in commands]
commands = sorted([command[len(prefix):] for command in commands])

ignored_commands = set() # type: Set[str]

def get_short_help(command:str) -> str:
	short_help = {
		"course": "Deal with Moodle courses",
		"remote": "Manage Moodle remotes",
	}
	try:
		return short_help[command]
	except KeyError:
		return ""

commands = [command for command in commands if command not in ignored_commands]

width = max([len(command) for command in commands]) + 2
epilog = "Available commands:\n{0}".format("\n".join(["   " + command.ljust(width) + " " + get_short_help(command) for command in commands]))

parser = argparse.ArgumentParser(description="Commandline client for Moodle", epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('commmand', help="The command to be invoked.").completer = lambda **kwargs: commands # type: ignore
parser.add_argument('args', nargs='*', help="Further command-specific arguments.")

if len(sys.argv) == 1:
	parser.print_help()
	sys.exit(0)

# Manually filter -h that was meant for a command
argv = sys.argv
command_help = []
if len(argv) > 2:
	if argv[2] == '-h' or argv[2] == '--help':
		command_help = ['-h']
		del argv[2]

args = parser.parse_known_args(argv)

command = argv[1]

if command not in commands:
	sys.exit(progname + ": '" + command + "' is not a moodle command.")

real_command = os.path.join(scriptdir, prefix + command)

subprocess.call([real_command] + command_help + argv[2:])
