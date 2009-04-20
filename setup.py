#!/usr/bin/env python

import os

from setuptools import setup

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == "":
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

bosnobot_dir = "bosnobot"

packages = []
for dirpath, dirnames, filenames in os.walk(bosnobot_dir):
    # ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith("."):
            del dirnames[i]
    if "__init__.py" in filenames:
        packages.append(".".join(fullsplit(dirpath)))

setup(
    name = "bosnobot",
    version = "1.0-beta",
    description = "Python IRC bot",
    author = "Brian Rosner",
    author_email = "brosner@gmail.com",
    url = "http://github.com/brosner/bosnobot/",
    packages = packages,
)
