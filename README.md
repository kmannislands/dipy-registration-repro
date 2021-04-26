# Dipy Platform inconsistency reproduction

## Install and run on macOs

- Install poetry (recommended version: `1.0.8`)
- Use poetry to install dependencies in venv:
  `poetry install`
- Run the test locally:
  `poetry run pytest`

## Install and run docker

- Ensure you have docker installed
- Build the testing image with poetry-managed dependencies:
  `docker build --file ./docker/Dockerfile --target test . --tag dipy_repro`
- Run the test in docker:
  `docker run dipy_repro`
