FROM python:3.12 as app
WORKDIR /app
RUN apt update && apt install pipx -y --no-install-recommends && apt-get clean all
RUN pipx install poetry

ENV PATH="${PATH}:/root/.local/bin"

COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
RUN poetry install -vvv --compile --without dev --no-root && poetry -n cache clear --all .

COPY . .

ENTRYPOINT ["poetry", "run", "app"]