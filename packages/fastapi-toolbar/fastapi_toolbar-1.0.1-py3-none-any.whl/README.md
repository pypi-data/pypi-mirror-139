## Welcome to FastAPI-Toolbar

[![PyPI](https://img.shields.io/pypi/v/stela)](https://pypi.org/project/fastpi-toolbar/)
[![Build](https://github.com/chrismaille/fastpi-toolbar/workflows/tests/badge.svg)](https://github.com/chrismaille/fastpi-toolbar/actions)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastpi-toolbar)](https://www.python.org)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)


> Original work: https://github.com/mongkok/fastapi-debug-toolbar

### Installation

```sh
pip install fastapi-toolbar
```

### Quickstart

Add `DebugToolbarMiddleware` middleware to your FastAPI application:

```py
from debug_toolbar.middleware import DebugToolbarMiddleware
from fastapi import FastAPI

app = FastAPI(debug=True)
app.add_middleware(DebugToolbarMiddleware)
```

### SQLAlchemy

Please make sure to use the *"Dependency Injection"* system as described in the [FastAPI docs](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency) and add the `SQLAlchemyPanel` to your panel list:

If you're using a database session generator (using `yield`), please add the full python path of your generators
on the `session_generators` options, when adding the middleware:

```python
# database.py
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # sqlite will drop tables in memory
        Base.metadata.create_all(bind=engine)  # create tables again
```

```py
# app.py
from fastapi import FastAPI
from debug_toolbar.middleware import DebugToolbarMiddleware

app = FastAPI()

app.add_middleware(
    DebugToolbarMiddleware,
    panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],
    session_generators=["database:get_db"]  # Add the full python path of your session generators
)
```

### Tortoise ORM

Add the `TortoisePanel` to your panel list:

```py
from fastapi import FastAPI
from debug_toolbar.middleware import DebugToolbarMiddleware

app = FastAPI()

app.add_middleware(
    DebugToolbarMiddleware,
    panels=["debug_toolbar.panels.tortoise.TortoisePanel"],
)
```
