FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /code/

# Copy dependency definition files and install dependencies first for better caching
COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen

# Copy the rest of the application code
COPY . .

# Install system-level build dependencies
RUN set -ex \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        gettext \
        libjpeg-dev \
        libpq-dev \
        make \
        postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expose the application port
EXPOSE 8000

# Set environment variables for the entrypoint script
# and add the virtual environment to the PATH. This is the key fix.
ENV DJANGO_MANAGEPY_MIGRATE=on \
    DJANGO_MANAGEPY_COLLECTSTATIC=on \
    DJANGO_MANAGEPY_UPDATEINDEX=on \
    PATH="/code/.venv/bin:$PATH"

# Set the entrypoint
ENTRYPOINT ["/code/docker-entrypoint.sh"]

# Set the default command to run the development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
