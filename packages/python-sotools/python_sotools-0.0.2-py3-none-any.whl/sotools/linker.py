"""
Implementation of the dynamic linker search algorithm
Rules in ld.so(8)
"""

import os
import re
from logging import error
from tempfile import NamedTemporaryFile
from functools import lru_cache
from pathlib import Path

from shutil import which
from subprocess import run, PIPE


class LinkingError(Exception):
    pass


def host_libraries(regen_cache=False):
    """
    Output a dict containing all the host's linker cache in x86_64 format
    under the format {soname: path}
    """
    # The versions that appear in `ldconfig -p`
    # For some reason, ppc shows '64bits'
    valid_versions = {'64bit', 'x86-64'}

    ldconfig_path = which('ldconfig')
    if ldconfig_path is None:
        error("ldconfig executable not found")
        return {}

    tmp_cache = NamedTemporaryFile('r+')
    cache_args = ['-C', tmp_cache.name] if regen_cache else []

    if regen_cache:
        regen = run([ldconfig_path, *cache_args], capture_output=False)

        if regen.returncode:
            error(
                f"Cache generation failed with returncode {regen.returncode}")
            cache_args = []

    cache = run([ldconfig_path, *cache_args, '-p'],
                stdout=PIPE,
                stderr=PIPE,
                encoding='utf-8')

    if cache.returncode:
        error(f"Error reading library cache using {ldconfig_path}")
        return {}

    _cache = {}

    for row in cache.stdout.split('\n')[1:]:
        # Expecting format "\t\tlibname.so.y (libc,arch) => /path/libname.so.y"
        pattern = r'^\s+(?P<soname>\S+(\.\S+)+).*\((?P<details>.*)\).*?(?P<path>(\/\S+)+)$'

        match = re.match(pattern, row)
        if not match:
            continue

        # Check the `arch` from above
        # Sometimes there is no data, so handle that case
        details = match.group('details').split(',')
        if len(details) < 2 or details[1] not in valid_versions:
            continue

        _cache[match.group('soname')] = match.group('path')

    return _cache


@lru_cache()
def _linker_path():
    """
    Return linker search paths, in order
    Sourced from `man ld.so`
    """
    default_path = ['/lib', '/usr/lib', '/lib64', '/usr/lib64']
    ld_library_path = os.environ.get('LD_LIBRARY_PATH', "").split(':')

    return (ld_library_path, default_path)


def resolve(soname, rpath=None, runpath=None):
    """
    Get a path towards a library from a given soname.
    Implements system rules and takes the environment into account
    """

    found = None
    rpath = rpath or []
    runpath = runpath or []

    def _valid(path):
        return os.path.exists(path) and os.path.isdir(path)

    dynamic_paths = list(rpath) + _linker_path()[0] + list(runpath)
    default_paths = _linker_path()[1]

    for dir_ in filter(_valid, dynamic_paths):
        potential_lib = Path(dir_, soname).as_posix()
        if os.path.exists(potential_lib):
            found = potential_lib

    if not found and soname in host_libraries().keys():
        found = host_libraries()[soname]

    if not found:
        for dir_ in filter(_valid, default_paths):
            potential_lib = Path(dir_, soname).as_posix()
            if os.path.exists(potential_lib):
                found = potential_lib

    return os.path.realpath(found) if found else None
