# backend

A repository storing code our API.

## Local development

### Python environment

How to install python dependencies using conda. You can use any other virtual environment.

> Install [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

```bash
conda create -n my-virtual-env python=3.10

conda activate my-virtual-env

pip install -r requirements.txt
```

### Docker compose

Allows to run dokerized backend and database for testing purposes.

> You need to have [Docker](https://www.docker.com/) installed.

Run:

```bash
docker compose up
```

To rebuild images, run:

```bash
docker compose build
```

## Running unit tests 

How to run unit tests locally.

Create a docker container with database:

```bash
docker compose up database
```

Open a second bash terminal and run pytest:

```bash
pytest -vv
```
Generate html code coverage report:

```bash
pytest -vv --cov --cov-report html
```

Open `htmlcov/index.html` with web browser.
