#!/usr/bin/env python3
"""pyfltr。"""
from __future__ import annotations

import argparse
import os
import pathlib
import shlex
import subprocess
import sys
import threading
import typing

import joblib
import tomli

CONFIG: dict[str, typing.Any] = {
    "pyupgrade_args": ["pyupgrade"],
    "pyupgrade_check_args": [],
    "pyupgrade_globs": ["*.py", "**/*.py"],
    "isort_args": ["isort"],
    "isort_check_args": ["--check"],
    "isort_globs": ["*.py", "**/*.py"],
    "black_args": ["black"],
    "black_check_args": ["--check"],
    "black_globs": ["*.py", "**/*.py"],
    "pflake8_args": ["pflake8"],
    "pflake8_check_args": [],
    "pflake8_globs": ["*.py", "**/*.py"],
    "mypy_args": ["mypy"],
    "mypy_check_args": [],
    "mypy_globs": ["*.py", "**/*.py"],
    "pylint_args": ["pylint"],
    "pylint_check_args": [],
    "pylint_globs": ["*.py", "**/*.py"],
    "pytest_args": ["pytest"],
    "pytest_check_args": [],
    "pytest_globs": ["*_test.py", "**/*_test.py"],
    "exclude": [],
}

ALL_COMMANDS = ["pyupgrade", "isort", "black", "pflake8", "mypy", "pylint", "pytest"]

lock = threading.Lock()


def main(args: typing.Sequence[str] = None):
    """エントリポイント。"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", default=False, action="store_true", help="`--check` for black/isort."
    )
    parser.add_argument(
        "--commands",
        default=",".join(ALL_COMMANDS),
        help=f'comma separated list of commands. (default: {",".join(ALL_COMMANDS)})',
    )
    parser.add_argument(
        "targets",
        nargs="*",
        type=pathlib.Path,
        help="target files and/or directories. (default: .)",
    )
    args = parser.parse_args(args)

    # pyproject.toml
    pyproject_path = pathlib.Path("pyproject.toml").absolute()
    if pyproject_path.exists():
        print(f"config: {pyproject_path}")
        pyproject_data = tomli.loads(
            pyproject_path.read_text(encoding="utf-8", errors="backslashreplace")
        )
        for key, value in pyproject_data.get("tool", {}).get("pyfltr", {}).items():
            if key not in CONFIG:
                print(f"Invalid config key: {key}", file=sys.stderr)
                return 1
            if not isinstance(value, type(CONFIG[key])):  # 簡易チェック
                print(
                    f"invalid config value: {key}={type(value)}"
                    f", expected {type(CONFIG[key])}",
                    file=sys.stderr,
                )
                return 1
            CONFIG[key] = value

    # run
    jobs: typing.Any = []
    for command in args.commands.split(","):
        if f"{command}_args" not in CONFIG:
            parser.error(f"command not found: {command}")
        jobs.append(joblib.delayed(run_command)(command, args.check, args.targets))
    with joblib.Parallel(n_jobs=len(jobs), backend="threading") as parallel:
        returncodes = parallel(jobs)

    # returncode
    return 0 if all(returncode == 0 for returncode in returncodes) else 1


def run_command(command: str, check: bool, targets: list[pathlib.Path]) -> int:
    """コマンドの実行。"""
    commandline = CONFIG[f"{command}_args"].copy()
    if check:
        commandline.extend(CONFIG[f"{command}_check_args"])
    commandline.extend(map(str, _expand_globs(targets, CONFIG[f"{command}_globs"])))
    return _execute_command(command, commandline)


def _execute_command(command: str, commandline: list[str]) -> int:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        commandline,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
        text=True,
        encoding="utf-8",
        errors="backslashreplace",
    )

    ncols = 128
    mark = "*" if proc.returncode == 0 else "@"
    output = f"""{mark * 32} {command} {mark * (ncols - 34 - len(command))}
{mark} commandline: {' '.join(shlex.quote(a) for a in commandline)}
{mark}
{proc.stdout.strip()}
{mark}
{mark} returncode: {proc.returncode}
{mark * ncols}
"""
    with lock:
        sys.stdout.buffer.write(
            output.encode(encoding=sys.stdout.encoding, errors="backslashreplace")
        )
        sys.stdout.flush()

    return proc.returncode


def _expand_globs(targets: list[pathlib.Path], globs: list[str]) -> list[pathlib.Path]:
    # 空ならカレントディレクトリを対象とする
    if len(targets) == 0:
        targets = [pathlib.Path(".")]

    expanded: set[pathlib.Path] = set()
    for target in targets:
        if _excluded(target):
            continue
        if target.is_dir():
            # ディレクトリの場合、globsのいずれかに一致するファイルをリストアップ
            for glob in globs:
                for child in target.glob(glob):
                    if _excluded(child):
                        continue
                    expanded.add(child)
        else:
            # ファイルの場合、globsのいずれかに一致するなら追加
            if any(target.match(glob) for glob in globs):
                expanded.add(target)

    return list(expanded)


def _excluded(path: pathlib.Path):
    for glob in CONFIG["exclude"]:
        if path.match(glob):
            return True
    return False


if __name__ == "__main__":
    main()
