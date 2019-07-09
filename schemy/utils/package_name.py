import re

from schemy.utils.storage import Storage

__all__ = ['package_name']

def package_name(file):
    """Given a path to a setup.py try to return the package name"""
    pattern = re.compile("name=([0-9A-Za-z_']+)")
    name = None
    with Storage(file, 'r') as setup:
        found = pattern.search(setup.content)
        if found:
            name = found.group(1).strip("'")
    return name
