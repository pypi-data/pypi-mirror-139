# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['debug_toolbar', 'debug_toolbar.panels']

package_data = \
{'': ['*'],
 'debug_toolbar': ['statics/css/*',
                   'statics/img/*',
                   'statics/js/*',
                   'templates/*',
                   'templates/includes/*',
                   'templates/panels/*']}

install_requires = \
['Jinja2', 'aiofiles', 'anyio', 'fastapi', 'pyinstrument', 'sqlparse']

setup_kwargs = {
    'name': 'fastapi-toolbar',
    'version': '1.0.1',
    'description': 'A debug toolbar for FastAPI.',
    'long_description': '## Welcome to FastAPI-Toolbar\n\n[![PyPI](https://img.shields.io/pypi/v/stela)](https://pypi.org/project/fastpi-toolbar/)\n[![Build](https://github.com/chrismaille/fastpi-toolbar/workflows/tests/badge.svg)](https://github.com/chrismaille/fastpi-toolbar/actions)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastpi-toolbar)](https://www.python.org)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n\n> Original work: https://github.com/mongkok/fastapi-debug-toolbar\n\n### Installation\n\n```sh\npip install fastapi-toolbar\n```\n\n### Quickstart\n\nAdd `DebugToolbarMiddleware` middleware to your FastAPI application:\n\n```py\nfrom debug_toolbar.middleware import DebugToolbarMiddleware\nfrom fastapi import FastAPI\n\napp = FastAPI(debug=True)\napp.add_middleware(DebugToolbarMiddleware)\n```\n\n### SQLAlchemy\n\nPlease make sure to use the *"Dependency Injection"* system as described in the [FastAPI docs](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-dependency) and add the `SQLAlchemyPanel` to your panel list:\n\nIf you\'re using a database session generator (using `yield`), please add the full python path of your generators\non the `session_generators` options, when adding the middleware:\n\n```python\n# database.py\nfrom typing import Generator\nfrom sqlalchemy import create_engine\nfrom sqlalchemy.ext.declarative import declarative_base\nfrom sqlalchemy.orm import sessionmaker\n\nengine = create_engine("sqlite://", connect_args={"check_same_thread": False})\nSessionLocal = sessionmaker(bind=engine)\nBase = declarative_base()\n\nBase.metadata.create_all(bind=engine)\n\ndef get_db() -> Generator:\n    db = SessionLocal()\n    try:\n        yield db\n    finally:\n        db.close()  # sqlite will drop tables in memory\n        Base.metadata.create_all(bind=engine)  # create tables again\n```\n\n```py\n# app.py\nfrom fastapi import FastAPI\nfrom debug_toolbar.middleware import DebugToolbarMiddleware\n\napp = FastAPI()\n\napp.add_middleware(\n    DebugToolbarMiddleware,\n    panels=["debug_toolbar.panels.sqlalchemy.SQLAlchemyPanel"],\n    session_generators=["database:get_db"]  # Add the full python path of your session generators\n)\n```\n\n### Tortoise ORM\n\nAdd the `TortoisePanel` to your panel list:\n\n```py\nfrom fastapi import FastAPI\nfrom debug_toolbar.middleware import DebugToolbarMiddleware\n\napp = FastAPI()\n\napp.add_middleware(\n    DebugToolbarMiddleware,\n    panels=["debug_toolbar.panels.tortoise.TortoisePanel"],\n)\n```\n',
    'author': 'Dani',
    'author_email': 'dani@domake.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chrismaille/fastapi-toolbar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
