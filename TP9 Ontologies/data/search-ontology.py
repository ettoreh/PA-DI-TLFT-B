from owlready2 import *


onto = get_ontology("TP9 Ontologies/data/wildlife-en.xml").load()
sync_reasoner([onto])

print("Here are classes and their IRIs:")
for cl in onto.classes():
    print(cl.name,cl.iri)
    
print("###\nFind class animal")
r = onto.search(iri="*#animal")
print(r)

print("###\nFind classes ending with plant")
r = onto.search(iri="*#*plant")
print(r)

print("###\nFind sublclasses of the class animal")
r = onto.search(subclass_of = onto.search(iri="*#animal")[0])
print(r)

print("###\nFind the individuals of the second animal subclass")
r = onto.search(type = onto.search(subclass_of = onto.search(iri="*#animal")[0])[1])
print(r)

print("###\nFind all animals")
r = onto.search(type = onto.search(iri="*#animal")[0])
print(r)

print("###\nFind all individuals weighting 800")
r = onto.search(weight = 800)
print(r)

print("###\nFind who eats Gigi")
r = onto.search(eats = onto.search(iri="*Gigi")[0])
print(r)

print("###\nFind who makes what with whom")
for ind in onto.individuals():
    for rol in onto.object_properties():
        if rol[ind]:
            for suc in rol[ind]:
                print(ind.iri,rol.name,suc.iri)
