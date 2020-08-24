#!/usr/bin/env python3
#
# (c) 2020 by Sebastian Bauer
#
# This simple script takes the ReadMe.md file as input and regenerates
# the "Commands" sections using "bin/moodle"
#
from subprocess import check_output

import sys
import string

if len(sys.argv) < 2:
	sys.exit("No input given")

f = open(sys.argv[1],"r")
lines = f.readlines()

out = check_output(["bin/moodle"],universal_newlines=True)

state = 0

for line in lines:
	line = line.rstrip()
	if line == 'Commands' and state == 0:
		state = 1
	elif line == '--------' and state == 1:
		state = 2
	elif state == 2:
		state = 3
	elif line.startswith('---') and state == 3:
		state = 4
	elif state == 4:
		state = 5

	if state == 2:
		print(line)
		print()
		print("```")
		print(out)
		print("```\n")
	elif state == 4:
		print(prev_line)
		print(line)
	elif state != 3:
		print(line)

	prev_line = line
