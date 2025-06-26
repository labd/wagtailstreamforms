.PHONY: install test upload docs


install:
	pip install -e .[docs,test]

test:
	DJANGO_SETTINGS_MODULE=tests.settings ./manage.py test

retest:
	py.test --nomigrations --reuse-db --lf --ignore=tests/functional tests/

docs:
	$(MAKE) -C docs html

format:
	ruff check --fix wagtailstreamforms/ tests/
	ruff format wagtailstreamforms/ tests/

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
