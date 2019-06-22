#
# Generic data bindings for the schema to use
#

import os
import errno
import rrdtool
from collections import namedtuple

from config import RRDPATH

rrdfile = namedtuple("rrdfile", ["inum", "name", "path"])


def get_rrdseries(path, start_time=None, end_time=None, CF="AVERAGE"):
    _rrdargs = []
    if start_time:
        int(start_time)
        _rrdargs.extend(["-s", "{}".format(start_time)])
    if end_time:
        int(end_time)
        _rrdargs.extend(["-e", "{}".format(end_time)])

    _series = {}
    _path = os.path.normpath(path)
    if not os.path.isabs(_path):
        _path = os.path.join(RRDPATH, _path)
    try:
        _meta, _name, _data = rrdtool.fetch(str(_path), str(CF), *_rrdargs)
        istart, iend, istep = _meta
        for n in _name:
            _series[n] = []
        for i, vals in enumerate(_data):
            for j in range(len(_name)):
                if vals[j] != None:
                    _pair = { "t": istart + i * istep, "v": vals[j]}
                    _series[_name[j]].append(_pair)
    except Exception as excn:
        print str(excn)
        pass
    return _series


def get_rrdfile(inum, path):
    _path = os.path.join(RRDPATH, path)
    if os.path.exists(_path):
        _inum = os.stat(_path).st_ino
        if inum == _inum:
            return rrdfile(_inum, os.path.basename(_path), _path)
    return None


def get_rrdfiles():
    _files = []
    for directory, subdirs, files in os.walk(RRDPATH):
        for _file in files:
            if _file.endswith(".rrd"):
                _path = os.path.join(directory, _file)
                _inum = os.stat(_path).st_ino
                _path = os.path.relpath(_path, RRDPATH)
                _files.append(rrdfile(_inum, _file, _path))
    return _files
