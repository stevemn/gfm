from datasets import Datum

def shortId(res=None, val=None):
	return Datum(res,'<http://vivo.brown.edu/ontology/vivo-brown/shortId>', val)