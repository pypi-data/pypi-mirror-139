# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kjst_kuku']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.1,<2.0.0', 'plotly>=5.6.0,<6.0.0', 'typer>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['kjst-kuku = kjst_kuku.main:app']}

setup_kwargs = {
    'name': 'kjst-kuku',
    'version': '0.1.3',
    'description': '',
    'long_description': 'kjst-kuku\n=========\n\n掛け算ドリル\n\nInstall\n-------\n\n```sh\npython -m pip install --upgrade git+https://github.com/kenjisato/kjst-kuku\n```\n\nUsage\n-----\n\n### 3の段を順番に出題\n\n```sh\nkjst-kuku start -o 3\n```\n\n### 5の段のシャッフル\n\n```sh\nkjst-kuku start 5\n```\n\n### 全部をシャッフル\n\n```sh\nkjst-kuku start\n```\n\n### 3, 4, 6, 8の段をシャッフルしない\n\n```sh\nkjst-kuku start -o 3-4/6-8\n```\n\n\nShow Records\n------------\n\nHelper commands will come soon. Until then, see \n\n```sh\ncat ~/.kuku_records\n```\n',
    'author': 'Kenji Sato',
    'author_email': 'mail@kenjisato.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
