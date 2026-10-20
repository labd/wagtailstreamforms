.PHONY: install test tox docs format lint makemessages compilemessages build

install:
	uv sync --all-groups

test:
	uv run python manage.py test --settings=tests.settings

tox:
	uvx --with tox-uv tox run-parallel

docs:
	uv run --group docs $(MAKE) -C docs html

format:
	uv run ruff check --fix --select I wagtailstreamforms/ tests/
	uv run ruff format wagtailstreamforms/ tests/

lint:
	uv run ruff format --check wagtailstreamforms/ tests/
	uv run ruff check wagtailstreamforms/ tests/

#
# Utility
makemessages:
	cd wagtailstreamforms && uv run django-admin makemessages --all

compilemessages:
	cd wagtailstreamforms && uv run django-admin compilemessages

build:
	uv build
