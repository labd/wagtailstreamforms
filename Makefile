.PHONY: install test upload docs


install:
	pip install -e .[docs,test]

test:
	DJANGO_SETTINGS_MODULE=tests.settings ./manage.py test

docs:
	$(MAKE) -C docs html

format:
	isort --recursive wagtailstreamforms tests
	black wagtailstreamforms/ tests/

#
# Utility
makemessages:
	./manage.py makemessages -all

compilemessages:
	./manage.py compilemessages

release:
	rm -rf dist/*
	python setup.py sdist bdist_wheel
	twine upload dist/*
