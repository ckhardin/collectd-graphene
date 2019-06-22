#
# Generic data bindings for the schema to use
#

import os
import errno
import rrdtool
from collections import namedtuple

from config import RRDPATH

rrdfile = namedtuple("rrdfile", ["inum", "name", "path"])
plugin = namedtuple("plugin", ["inum", "name", "path"])
plugin_data = namedtuple("plugin_data", ["inum", "plugin",
                                         "instance", "series"])


def get_rrdseries(path, start_time=None, end_time=None, CF="AVERAGE"):
    _rrdargs = []
    if start_time:
        int(start_time)
        _rrdargs.extend(["-s", "{}".format(start_time)])
    if end_time:
        int(end_time)
        _rrdargs.extend(["-e", "{}".format(end_time)])

    _series = []
    _path = os.path.normpath(path)
    if not os.path.isabs(_path):
        _path = os.path.join(RRDPATH, _path)
    _inum = os.stat(_path).st_ino
    try:
        _meta, _name, _data = rrdtool.fetch(str(_path), str(CF), *_rrdargs)
        istart, iend, istep = _meta
        for i,n in enumerate(_name):
            _series.append({ 'index': '{}.{}'.format(_inum, i),
                             'name': n, 'sequence': [] })
        for i,vals in enumerate(_data):
            _t = istart + i * istep
            for j in range(len(_name)):
                if vals[j] != None:
                    assert(_series[j].get('name') == _name[j])
                    _pair = { "t": _t, "v": vals[j] }
                    _series[j]['sequence'].append(_pair)
    except Exception as excn:
        print str(excn)
        pass
    return _series


def get_rrdfile(inum, path, rrdpath=RRDPATH):
    _path = os.path.join(rrdpath, path)
    if os.path.exists(_path):
        _inum = os.stat(_path).st_ino
        if inum == _inum:
            return rrdfile(_inum, os.path.basename(_path), _path)
    return None


def get_rrdfiles(rrdpath=RRDPATH):
    _files = []
    for directory, subdirs, files in os.walk(rrdpath):
        for _file in files:
            if _file.endswith(".rrd"):
                _path = os.path.join(directory, _file)
                _inum = os.stat(_path).st_ino
                _path = os.path.relpath(_path, rrdpath)
                _files.append(rrdfile(_inum, _file, _path))
    return _files


def get_plugin_data(path, rrdpath=RRDPATH):
    _plugin_instance = os.path.basename(path)
    _plugin_id = _plugin_instance.partition('-')[0]
    _plugin_series = []
    _path = os.path.join(rrdpath, path)
    _plugin_inum = os.stat(_path).st_ino
    for directory, subdirs, files in os.walk(_path):
        for _file in files:
            if _file.endswith(".rrd"):
                # get the type instance
                _series = get_rrdseries(os.path.join(directory, _file))
                _type_instance = str(_file)[:-len(".rrd")]
                (_type, _, _typei) = _type_instance.partition('-')
                for s in _series:
                    _name = s.get('name')
                    if _typei:
                        s.update({'name': "{}-{}".format(_typei, _name)})
                    else:
                        s.update({'name': "{}-{}".format(_type, _name)})
                _plugin_series.extend(_series)
    return plugin_data(inum=_plugin_inum, plugin=_plugin_id,
                       instance=_plugin_instance, series=_plugin_series)


def get_plugin(inum, path, rrdpath=RRDPATH):
    _path = os.path.join(rrdpath, path)
    if os.path.exists(_path):
        _inum = os.stat(_path).st_ino
        if inum == _inum:
            return plugin(_inum, os.path.basename(_path), _path)
    return None


def get_plugins(rrdpath=RRDPATH):
    _plugins = {}
    for directory, subdirs, files in os.walk(rrdpath):
        for _file in files:
            if _file.endswith(".rrd"):
                _instance = directory
                _inum = os.stat(_instance).st_ino
                _instance = os.path.relpath(_instance, rrdpath)
                if not _instance in _plugins:
                    _plugin = plugin(_inum, os.path.basename(directory),
                                     _instance)
                    _plugins[_instance] = _plugin
    return _plugins.values()
