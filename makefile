.PHONY: all
all: type-check

.PHONY: update-readme
update-readme:
	rm -f ReadMe.md.tmp
	devscripts/update-readme.py ReadMe.md >ReadMe.md.tmp
	mv ReadMe.md.tmp ReadMe.md

.PHONY: type-check
type-check:
	mypy --scripts-are-modules $(wildcard bin/moodle-*) $(wildcard bin/*.py)
