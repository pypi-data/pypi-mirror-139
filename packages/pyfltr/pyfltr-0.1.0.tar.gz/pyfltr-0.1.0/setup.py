# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfltr']

package_data = \
{'': ['*']}

install_requires = \
['black',
 'flake8-bugbear',
 'isort',
 'joblib',
 'mypy',
 'pylint',
 'pyproject-flake8',
 'pytest',
 'pyupgrade',
 'tomli']

entry_points = \
{'console_scripts': ['pyfltr = pyfltr.pyfltr:main']}

setup_kwargs = {
    'name': 'pyfltr',
    'version': '0.1.0',
    'description': 'pyfltr: Python Formatter, Linter, and Tester Runner.',
    'long_description': '# pyfltr: Python Formatters, Linters, and Testers Runner.\n\n[![Lint&Test](https://github.com/ak110/pyfltr/actions/workflows/python-app.yml/badge.svg)](https://github.com/ak110/pyfltr/actions/workflows/python-app.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nPythonの各種ツールを呼び出すスクリプト。\n\n## 対象ツール\n\n- pyupgrade\n- isort\n- black\n- pflake8\n- mypy\n- pylint\n- pytest\n\n## 使い方\n\n### 通常\n\n```text\nusage: pyfltr [targets ...]\n```\n\n全ツールを実行する。\n\n### CIなど用\n\n```text\nusage: pyfltr --check [targets ...]\n```\n\n全ツールを実行する。isortとblackは`--check`付き。\n\n### 特定のコマンドのみ実行\n\n```text\nusage: pyfltr --commands=pyupgrade,isort,black,pflake8,mypy,pylint,pytest [targets ...]\n```\n\nカンマ区切りで実行するものだけ指定する。\n\n## 設定(pyproject.toml)\n\n挙動を変更したい場合は設定する。(以下は既定値)\n\n```toml\n[tool.pyfltr]\npyupgrade_args = ["pyupgrade"]\npyupgrade_check_args = []\npyupgrade_globs = ["*.py", "**/*.py"]\nisort_args = ["isort"]\nisort_check_args = ["--check"]\nisort_globs = ["*.py", "**/*.py"]\nblack_args = ["black"]\nblack_check_args = ["--check"]\nblack_globs = ["*.py", "**/*.py"]\npflake8_args = ["pflake8"]\npflake8_check_args = []\npflake8_globs = ["*.py", "**/*.py"]\nmypy_args = ["mypy"]\nmypy_check_args = []\nmypy_globs = ["*.py", "**/*.py"]\npylint_args = ["pylint"]\npylint_check_args = []\npylint_globs = ["*.py", "**/*.py"]\npytest_args = ["pytest"]\npytest_check_args = []\npytest_globs = ["*_test.py", "**/*_test.py"]\nexclude = []\n```\n\n- {command}_args : コマンドライン\n- {command}_check_args : --check時の追加のコマンドライン\n- {command}_globs : 対象のファイル名パターン\n- exclude : 除外するファイル名パターン\n',
    'author': 'aki.',
    'author_email': 'mark@aur.ll.to',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ak110/pyfltr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
