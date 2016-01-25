from datasets import Dataset, Datum
import types

TruthType = (types.NoneType, types.BooleanType)

SingleType = (types.StringType, types.UnicodeType,
                types.IntType, types.LongType,
                types.FloatType, types.ComplexType)

ListType = types.ListType

def get_objects(tset):
	return [ d[2] for d in dset ]

class MultiValued(object):
	def __init__(self, predicate):
		self.predicate = predicate

	def __get__(self, instance, cls):
		if instance:
			pattern = self.predicate(
				sbj=instance.node, obj=None)
			return get_objects(instance.graph.find(pattern))
		else:
			return self.predicate(sbj=None, obj=None)
		

	def __set__(self, instance, value):
		if not value or isinstance(value, TruthType):
			self.__delete__(instance)
			return
		elif isinstance(value, SingleType):
			self.__delete__(instance)
			add = { self.predicate(
            			sbj=instance.node, obj=value) }
		elif isinstance(value, ListType):
			self.__delete__(instance)
			add = { self.predicate(
						sbj=instance.node, obj=v)
							for v in value }
		else:
			raise Exception(
					"expected iterable, string or num")
		instance.graph.update(add)

	def __delete__(self, instance):
		pattern = self.predicate(sbj=instance.node, obj=None)
		rmv = set_filter(instance.graph, pattern)
		instance.graph.difference_update(rmv)

	# def add(self, instance, value):
	# 	instance.graph.add(self.predicate(sbj=instance.node, obj=value))

	# def remove(self, instance, value):
	# 	instance.graph.discard(self.predicate(sbj=instance.node, obj=value))