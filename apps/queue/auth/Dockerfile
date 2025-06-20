ARG VERSION=3.12-slim-bookworm
FROM python:$VERSION AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code

# Install dependencies
ARG DEPENDENCIES=requirements/core.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=$DEPENDENCIES,target=$DEPENDENCIES  \
    python3 -m pip install -r $DEPENDENCIES 

# Create a non-privileged user 
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "$UID" \
    code

# ------------------------------------------------------------ #

FROM builder AS testing
USER code
COPY . .

EXPOSE ${API_PORT:-8080}

CMD ["python3", "main.py"]
