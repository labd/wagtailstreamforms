.PHONY: install test upload docs


install:
	pip install -e .[docs,test]

test:
	DJANGO_SETTINGS_MODULE=tests.settings ./manage.py test

docs:
	$(MAKE) -C docs html

format:
	isort --recursive src tests
	black src/ tests/

#
# Utility
makemessages:
	cd src/wagtailstreamforms && python ../../manage.py makemessages -all

compilemessages:
	cd src/wagtailstreamforms && python ../../manage.py compilemessages

release:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*
