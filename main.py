#!/usr/bin/env python

import subprocess
import sys

__author__ = 'd1_boy4h'

def run_command(cmd: list[str], desc: str) -> bool:
    print(f'\n📋 {desc}...')

    result = subprocess.run(cmd)

    if result.returncode >= 1:
        return False

    return True

def main():
    commands = [
        (['mypy', '.', '--ignore-missing-imports'], 'mypy проверка типов'),
    ]

    for cmd, desc in commands:
        if not run_command(cmd, desc):
            sys.exit(1)

    from .src.core import App

    app = App()
    app.run()

if __name__ == '__main__':
    main()
