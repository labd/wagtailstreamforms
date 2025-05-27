FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy the application code to the container:
RUN mkdir /code/
WORKDIR /code/
ADD . /code/

# Install all build deps:
RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        gettext \
        libjpeg-dev \
        libpq-dev \
        make \
        postgresql-client \
    || (cat /var/log/apt/term.log || true) \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN uv sync --frozen

# expose port
EXPOSE 8000

# Docker entrypoint:
ENV DJANGO_MANAGEPY_MIGRATE=on \
    DJANGO_MANAGEPY_COLLECTSTATIC=on \
    DJANGO_MANAGEPY_UPDATEINDEX=on

ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Start python runserver:
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
