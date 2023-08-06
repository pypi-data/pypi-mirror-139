# GSpaces

![PyPI - Status](https://img.shields.io/pypi/status/gspaces?style=for-the-badge) ![PyPI](https://img.shields.io/pypi/v/gspaces?style=for-the-badge) ![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/quintenstar/gspaces?style=for-the-badge) ![PyPI - License](https://img.shields.io/pypi/l/gspaces?style=for-the-badge)

Provides memory efficient collections for common spaces.
Including, drop-in replacement for Numpy's arange, linspace, logspace and geomspace functions.

https://pypi.org/project/gspaces/

## Installation

```console
pip install gspaces
```

## Usage

```python
import gspaces

start = 0
stop = 1000
step = 1

x = gspaces.arange(start, stop, step)

num = 100
x = gspaces.linspace(start, stop, num=num)
x = gspaces.logspace(start, stop, num=num, base=3)
x = gspaces.geomspace(start, stop, num=num)
```
