from collections import defaultdict
from graphattributes import Edge
from datasets import DataSet, Datum, Required, Linked, Optional
import properties

class Resource(object):
    def __init__(self, uri, sessionGraph):
        self.sessionGraph = sessionGraph
        self.uri = uri
        self.edges = {
            getattr(self.__class__,k).att: k
                for k, v in self.__class__.__dict__.items()
                    if isinstance(v, Edge)
        }

    def __getitem__(self, key):
        return getattr(self, self.edges.__getitem__(key))

    def __setitem__(self, key, value):
        setattr(self, self.edges.__getitem__(key), value)

    def __delitem__(self, key):
        delattr(self, self.edges.__getitem__(key))

    def update(self):
        pass

    def destroy(self):
        pass

    def setSession(self, graph):
        self.sessionGraph = graph

    def unsetGraph(self):
        self.sessionGraph = None

    @classmethod
    def pattern(cls, res=None):
        qset = DataSet([])
        for k in cls.__dict__.keys():
            att = getattr(cls,k)
            if isinstance(att, Required):
                qset.add(att._replace(res=res))
            elif isinstance(att, Optional):
                qset.add(att._replace(res=res))
            elif isinstance(att, Linked):
                qset.add(att._replace(val=res))
            else:
                continue
        return qset

    @classmethod
    def find(cls, uri, session):
        res = session.find(cls.pattern(uri))
        if res:
            rsc = cls(res, session)
            session.register(rsc)
            return rsc
        else:
            raise "Resource not found"

    @classmethod
    def find_all(cls, session):
        res = session.find_all(cls.pattern())
        if res:
            rscs = [ cls(r) for r in res ]
            for rsc in rscs:
                session.register(rsc)
            return rscs
        else:
            raise "Resources not found"

    @classmethod
    def new(cls, session, **params):
        uri = session.mint_new_uri(cls.prefix)
        rsc = cls(uri)
        session.register(rsc)
        rsc.update(**params)
        return rsc

    @classmethod
    def destroy(session, cls, uri):
        rsc = cls.find(uri)
        for k in rsc:
            del k
        graph.register(rsc)
        return rsc

    def to_dict(self):
        out = {"@id": self.uri}
        for e in self.edges:
            out[e] = self[e]
        return out

    # def __len__(self):
    #     return len(self.graph)   

class FisFaculty(Resource):
    rdfType = Edge(properties.rdfType,Required,
        values=[
            'http://vivoweb.org/ontology/core#FacultyMember',
            'http://vivo.brown.edu/ontology/vivo-brown/BrownThing'
            ])
    shortId = Edge(properties.blocalShortId, Required) 
    label = Edge(properties.rdfsLabel, Optional)
    first = Edge(properties.foafFirstName, Optional)
    last = Edge(properties.foafLastName, Optional)
    title = Edge(properties.vivoPreferredTitle, Optional)
