# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nb_workflows',
 'nb_workflows.auth',
 'nb_workflows.cmd',
 'nb_workflows.db',
 'nb_workflows.workflows']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'SQLAlchemy-serializer>=1.4.1,<2.0.0',
 'SQLAlchemy[asyncio]>=1.4.26,<2.0.0',
 'Unidecode>=1.3.2,<2.0.0',
 'WTForms>=2.3.3,<3.0.0',
 'aiohttp[speedups]>=3.7.4,<4.0.0',
 'aioredis[hiredis]>=2.0.1,<3.0.0',
 'alembic>=1.6.5,<2.0.0',
 'arrow>=1.2.0,<2.0.0',
 'asyncpg>=0.24.0,<0.25.0',
 'bokeh>=2.4.1,<3.0.0',
 'cityhash>=0.2.3,<0.3.0',
 'click>=8.0.1,<9.0.0',
 'cloudpickle>=2.0.0,<3.0.0',
 'cryptography>=36.0.1,<37.0.0',
 'cytoolz>=0.11.0,<0.12.0',
 'dateparser>=1.1.0,<2.0.0',
 'discord-webhook>=0.14.0,<0.15.0',
 'ipywidgets>=7.6.5,<8.0.0',
 'jupyter-server-proxy>=3.1.0,<4.0.0',
 'jupyterlab-code-formatter>=1.4.10,<2.0.0',
 'jupyterlab>=3.1.14,<4.0.0',
 'jupytext>=1.13.0,<2.0.0',
 'loky>=3.0.0,<4.0.0',
 'nbconvert>=6.2.0,<7.0.0',
 'papermill>=2.3.3,<3.0.0',
 'psycopg2-binary>=2.9.1,<3.0.0',
 'python-slugify>=5.0.2,<6.0.0',
 'pytz>=2021.1,<2022.0',
 'requests>=2.26.0,<3.0.0',
 'rq-scheduler>=0.11.0,<0.12.0',
 'rq>=1.10.0,<2.0.0',
 'sanic-ext>=21.9.0,<22.0.0',
 'sanic-jwt>=1.7.0,<2.0.0',
 'sanic-openapi>=21.6.1,<22.0.0',
 'sanic>=21.6.2,<22.0.0',
 'tabulate>=0.8.9,<0.9.0',
 'tqdm>=4.62.3,<5.0.0',
 'ujson>=4.2.0,<5.0.0',
 'uvloop>=0.16.0,<0.17.0',
 'webdav4[fsspec]>=0.9.3,<0.10.0',
 'xxhash>=2.0.2,<3.0.0']

entry_points = \
{'console_scripts': ['nb = nb_workflows.cli:cli']}

setup_kwargs = {
    'name': 'nb-workflows',
    'version': '0.2.0',
    'description': 'Schedule parameterized notebooks programmatically using cli or a REST API',
    'long_description': '# NB Workflows\n\n![readthedocs](https://readthedocs.org/projects/nb_workflows/badge/?version=latest)\n![PyPI - Format](https://img.shields.io/pypi/format/nb_workflows)\n![PyPI - Status](https://img.shields.io/pypi/status/nb_workflows)\n\n\n## Description \n\nIf SQL is a lingua franca for querying data, Jupyter should be a lingua franca for data explorations, model training, and complex and unique tasks related to data. \n\nThis workflow platform allows to run parameterized notebooks programmatically. Notebooks could be scheduled with cron syntax, by intervals, run by n times, only once or in time ranges (from 10am to 18pm).\n\nSo, the notebook is the main UI and the workflow job description.  \n\n### Goal\n\nEmpowering different data roles in a project to put code into production, simplifying the time required to do so. It enables people to go from a data exploration instance to an entirely pipeline deployed in production, using the same notebook file made by a data scientist, analyst or whatever role working with data in an iterative way.\n\n## How to run\n\n```\n# launch web process\n# swagger by default: http://localhost:8000/docs/swagger \nmake web \n```\n\n```\n# RQ Worker\nmake rqworker\n```\n\n```\n# RQScheduler (optional)\nmake rqscheduler\n```\n\n## Architecture\n\n![nb_workflows architecture](/docs/platform-workflows.jpg)\n\n## References & inspirations\n- [Notebook Innovation - Netflix](https://netflixtechblog.com/notebook-innovation-591ee3221233)\n- [Tensorflow metastore](https://www.tensorflow.org/tfx/guide/mlmd)\n- [Maintainable and collaborative pipelines](https://blog.jupyter.org/ploomber-maintainable-and-collaborative-pipelines-in-jupyter-acb3ad2101a7)\n\n',
    'author': 'nuxion',
    'author_email': 'nuxion@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nuxion/nb_workflows',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
