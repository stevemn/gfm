from graphview import ResourceView
from graphattributes import Edge, Required, Optional, Linked
from properties import skos, rdfs, rdf

class VocabTerm(ResourceView):
	rdfType = Edge(rdf.rdfType, Required,
    	values=['http://www.w3.org/2004/02/skos/core#Concept',
		'http://vivo.brown.edu/ontology/vivo-brown/ResearchArea'])
	label = Edge(rdfs.label, Required)
	related = Edge(skos.related, Optional)
	broader = Edge(skos.broader, Optional)
	narrower = Edge(skos.narrower, Optional)
	pref = Edge(skos.prefLabel, Optional)
	alt = Edge(skos.altLabel, Optional)
	hidden = Edge(skos.hiddenLabel, Optional)