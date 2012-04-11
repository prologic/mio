.PHONY: help clean docs packages tests

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  clean     to cleanup build and temporary files"
	@echo "  docs      to build the documentation"
	@echo "  packages  to build python source and egg packages"
	@echo "  tests     to run the test suite"

clean:
	@rm -rf build dist mio.egg-info
	@rm -rf .coverage coverage
	@rm -rf docs/build
	@find . -name '*.pyc' -delete
	@find . -name '*.pyo' -delete
	@find . -name '*~' -delete

docs:
	@make -C docs clean html

packages:
	@tools/mkpkgs -p python2.5
	@tools/mkpkgs -p python2.6

tests:
	@python -m tests.main
