# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyspark_vector_files']

package_data = \
{'': ['*']}

install_requires = \
['GDAL==3.4.0',
 'more-itertools>=8.12.0,<9.0.0',
 'pandas==1.2.4',
 'pyspark==3.1.2']

setup_kwargs = {
    'name': 'pyspark-vector-files',
    'version': '0.1.0',
    'description': 'Read vector files into a Spark DataFrame with geometry encoded as WKB.',
    'long_description': "[![CI](https://github.com/Defra-Data-Science-Centre-of-Excellence/pyspark-vector-files/actions/workflows/ci.yml/badge.svg)](https://github.com/Defra-Data-Science-Centre-of-Excellence/pyspark-vector-files/actions/workflows/ci.yml)\n\n# PySpark Vector Files\n\nRead vector files into a Spark DataFrame with geometry encoded as WKB.\n\n## Install\n\n### Within a Databricks notebook\n\n```sh\n%pip install git+https://github.com/Defra-Data-Science-Centre-of-Excellence/pyspark_vector_files\n```\n\n### From the command line\n\n```sh\npython -m pip install git+https://github.com/Defra-Data-Science-Centre-of-Excellence/pyspark_vector_files\n```\n\n## Local development\n\nTo ensure compatibility with [Databricks Runtime 9.1 LTS](https://docs.databricks.com/release-notes/runtime/9.1.html), this package was developed on a Linux machine running the `Ubuntu 20.04 LTS` operating system using `Python 3.8.8`, `GDAL 3.4.0`, and `spark 3.1.2`.\n\n### Install `Python 3.8.8` using [pyenv](https://github.com/pyenv/pyenv)\n\nSee the `pyenv-installer`'s [Installation / Update / Uninstallation](https://github.com/pyenv/pyenv-installer#installation--update--uninstallation) instructions.\n\nInstall Python 3.8.8 globally:\n\n```sh\npyenv install 3.8.8\n```\n\nThen install it locally in the repository you're using:\n\n```sh\npyenv local 3.8.8\n```\n\n### Install `GDAL 3.4.0`\n\nAdd the [UbuntuGIS unstable Private Package Archive (PPA)](https://launchpad.net/~ubuntugis/+archive/ubuntu/ubuntugis-unstable)\nand update your package list:\n\n```sh\nsudo add-apt-repository ppa:ubuntugis/ubuntugis-unstable \\\n    && sudo apt-get update\n```\n\nInstall `gdal 3.4.0`, I found I also had to install python3-gdal (even though\nI'm going to use poetry to install it in a virtual environment later) to\navoid version conflicts:\n\n```sh\nsudo apt-get install -y gdal-bin=3.4.0+dfsg-1~focal0 \\\n    libgdal-dev=3.4.0+dfsg-1~focal0 \\\n    python3-gdal=3.4.0+dfsg-1~focal0\n```\n\nVerify the installation:\n\n```sh\nogrinfo --version\n# GDAL 3.4.0, released 2021/11/04\n```\n\n### Install `poetry 1.1.13`\n\nSee poetry's [osx / linux / bashonwindows install instructions](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions)\n\n### Clone this repository\n\n```sh\ngit clone https://github.com/Defra-Data-Science-Centre-of-Excellence/pyspark_vector_files.git\n```\n\n### Install dependencies using `poetry`\n\n```sh\npoetry install\n```\n",
    'author': 'Ed Fawcett-Taylor',
    'author_email': 'ed.fawcett-taylor@defra.gov.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Defra-Data-Science-Centre-of-Excellence/pyspark-vector-files',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.9',
}


setup(**setup_kwargs)
