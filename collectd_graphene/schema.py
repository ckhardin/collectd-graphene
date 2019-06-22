import graphene
from graphene import relay

from data import (get_rrdfiles, get_rrdfile, get_rrdseries,
                  get_plugins, get_plugin, get_plugin_data)


class RRDPair(graphene.ObjectType):
    t = graphene.Float()
    v = graphene.Float()

class RRDSeries(graphene.ObjectType):
    """An rrdseries representation"""

    class Meta:
        interfaces = (relay.Node,)

    name = graphene.String()
    sequence = graphene.List(RRDPair, description="List of time/value pairs")

    @classmethod
    def get_node(cls, info, id_):
        return cls()

class RRDSeriesConnection(relay.Connection):
    class Meta:
        node = RRDSeries


class RRDFile(graphene.ObjectType):
    """An rrdfile for parsing"""

    class Meta:
        interfaces = (relay.Node,)

    name = graphene.String()
    path = graphene.String()

    @classmethod
    def get_node(cls, info, id_):
        f = get_rrdfile(id_, info['path'])
        return RRDFile(id=f.inum,name=f.name,path=f.path)

class RRDFileConnection(relay.Connection):
    class Meta:
        node = RRDFile


class PluginData(graphene.ObjectType):

    class Meta:
        interfaces = (relay.Node,)

    plugin = graphene.String()
    instance = graphene.String()
    series = graphene.List(RRDSeries)

    @classmethod
    def get_node(cls, info, id_):
        pd = get_plugin_data(info['path'])
        return PluginData(id=pd.inum,plugin=pd.plugin,
                          instance=pd.instance,series=pd.series)

class PluginDataConnection(relay.Connection):
    class Meta:
        node = PluginData


class PluginInstance(graphene.ObjectType):
    """Represents a plugin instance the directory data"""
    class Meta:
        interfaces = (relay.Node,)

    name = graphene.String()
    path = graphene.String()

    @classmethod
    def get_node(cls, info, id_):
        p = get_plugin(id_, info['path'])
        return PluginInstance(id=p.inum,name=p.name,path=p.path)

class PluginInstanceConnection(relay.Connection):
    class Meta:
        node = PluginInstance


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    rrdfiles = graphene.List(RRDFile)
    rrdseries = graphene.List(RRDSeries, path=graphene.String())
    plugins = graphene.List(PluginInstance)
    plugindata = graphene.Field(PluginData, path=graphene.String())

    def resolve_rrdfiles(self, info):
        return [RRDFile(id=f.inum,name=f.name,path=f.path)
                for f in get_rrdfiles()]

    def resolve_rrdseries(self, info, path):
        if path:
           _rrdseries = []
           _series = get_rrdseries(path)
           for s in _series:
               _sequence = [RRDPair(t=float(p['t']), v=float(p['v']))
                            for p in s.get('sequence', [])]
               _rrdseries.append(RRDSeries(id=s['index'],name=s['name'],
                                           sequence=_sequence))
           return _rrdseries
        return []

    def resolve_plugins(self, info):
        return [PluginInstance(id=p.inum,name=p.name,path=p.path)
                for p in get_plugins()]

    def resolve_plugindata(self, info, path):
        if path:
           _plugindata = get_plugin_data(path)
           _pluginseries = []
           for s in _plugindata.series:
               _sequence = [RRDPair(t=float(p['t']), v=float(p['v']))
                            for p in s.get('sequence', [])]
               _pluginseries.append(RRDSeries(id=s['index'],name=s['name'],
                                              sequence=_sequence))
           return PluginData(id=_plugindata.inum,
                             plugin=_plugindata.plugin,
                             instance=_plugindata.instance,
                             series=_pluginseries)
        return None

schema = graphene.Schema(query=Query)
