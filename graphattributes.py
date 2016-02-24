from datasets import DataSet, Datum
import types

TruthType = (types.NoneType, types.BooleanType)
ListType = types.ListType

def get_values(dset):
	return [ d[2] for d in dset ]

class Edge(object):
	def __init__(self, attr, edgetype, values=[None]):
		self.attr = attr
		self.edgetype = edgetype
		self.values = values

	def __get__(self, instance, cls):
		if instance:
			pattern = self.attr(
				res=instance.uri, val=None)
			return get_values(instance.graph.query(pattern))
		else:
			return [ self.edgetype(*(self.attr(res=None, val=v)))
						for v in self.values ]

	def __set__(self, instance, value):
		if not value or isinstance(value, TruthType):
			self.__delete__(instance)
			return
		elif isinstance(value, ListType):
			self.__delete__(instance)
			add = { self.attr(
						res=instance.uri, val=v)
							for v in value }
			instance.graph.update(add)
		else:
			raise Exception("expected list value")

	def __delete__(self, instance):
		pattern = self.attr(res=instance.uri, val=None)
		instance.graph.query_and_remove(pattern)

class Required(Datum):
	pass

class Linked(Datum):
	pass

class Optional(Datum):
	pass

class Exclude(Datum):
	pass

class Only(Datum):
	pass