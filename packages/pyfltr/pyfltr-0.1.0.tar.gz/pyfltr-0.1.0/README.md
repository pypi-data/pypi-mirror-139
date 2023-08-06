# pyfltr: Python Formatters, Linters, and Testers Runner.

[![Lint&Test](https://github.com/ak110/pyfltr/actions/workflows/python-app.yml/badge.svg)](https://github.com/ak110/pyfltr/actions/workflows/python-app.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Pythonの各種ツールを呼び出すスクリプト。

## 対象ツール

- pyupgrade
- isort
- black
- pflake8
- mypy
- pylint
- pytest

## 使い方

### 通常

```text
usage: pyfltr [targets ...]
```

全ツールを実行する。

### CIなど用

```text
usage: pyfltr --check [targets ...]
```

全ツールを実行する。isortとblackは`--check`付き。

### 特定のコマンドのみ実行

```text
usage: pyfltr --commands=pyupgrade,isort,black,pflake8,mypy,pylint,pytest [targets ...]
```

カンマ区切りで実行するものだけ指定する。

## 設定(pyproject.toml)

挙動を変更したい場合は設定する。(以下は既定値)

```toml
[tool.pyfltr]
pyupgrade_args = ["pyupgrade"]
pyupgrade_check_args = []
pyupgrade_globs = ["*.py", "**/*.py"]
isort_args = ["isort"]
isort_check_args = ["--check"]
isort_globs = ["*.py", "**/*.py"]
black_args = ["black"]
black_check_args = ["--check"]
black_globs = ["*.py", "**/*.py"]
pflake8_args = ["pflake8"]
pflake8_check_args = []
pflake8_globs = ["*.py", "**/*.py"]
mypy_args = ["mypy"]
mypy_check_args = []
mypy_globs = ["*.py", "**/*.py"]
pylint_args = ["pylint"]
pylint_check_args = []
pylint_globs = ["*.py", "**/*.py"]
pytest_args = ["pytest"]
pytest_check_args = []
pytest_globs = ["*_test.py", "**/*_test.py"]
exclude = []
```

- {command}_args : コマンドライン
- {command}_check_args : --check時の追加のコマンドライン
- {command}_globs : 対象のファイル名パターン
- exclude : 除外するファイル名パターン
