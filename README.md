# kv-store

[![ci](https://github.com/Kilo59/kv-store/workflows/ci/badge.svg)](https://github.com/Kilo59/kv-store/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Simple Key:Value storage and API

## Quick Start

Install python3.10
[Install `poetry`](https://python-poetry.org/docs/)

```
brew install poetry
```

Install dependencies

```
poetry install
```

Start api

```
poetry run invoke api
```

## Automated Tests

```
poetry run pytest -vv
```

## Usage

For usage instructions refer to the ReDoc UI.
If running locally visit http://127.0.0.1:8000/schema

Otherwise see the heroku deployment https://py-kv-store.herokuapp.com/schema
Note the heroku application may be asleep if not used recently. It make take a few seconds to boot up.

## TODO

- [x] API
- [x] Client
- [ ] CLI
- [ ] Dockerfiles
  - [ ] Server
  - [ ] Client
  - [ ] compose
