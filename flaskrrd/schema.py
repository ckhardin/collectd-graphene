import graphene
from graphene import relay

from data import get_rrdfiles, get_rrdfile, get_rrdseries


class RRDPair(graphene.ObjectType):
    t = graphene.Float()
    v = graphene.Float()


class RRDSeries(graphene.ObjectType):
    """An rrdseries representation"""

    class Meta:
        interfaces = (relay.Node,)

    label = graphene.String()
    sequence = graphene.List(RRDPair, description="A lit of time/value pairs")

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


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    rrdfiles = graphene.List(RRDFile)
    rrdseries = graphene.List(RRDSeries, path=graphene.String())

    def resolve_rrdfiles(self, info):
        return [RRDFile(id=f.inum,name=f.name,path=f.path)
                for f in get_rrdfiles()]

    def resolve_rrdseries(self, info, path):
        if path:
           i = 0
           _rrdseries = []
           _series = get_rrdseries(path)
           for x,y in sorted(_series.iteritems()):
               _sequence = [RRDPair(t=float(p['t']), v=float(p['v'])) for p in y]
               _rrdseries.append(RRDSeries(id=i,label=x,sequence=_sequence))
               i += 1
           return _rrdseries
        return []


schema = graphene.Schema(query=Query)