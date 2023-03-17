from owlready2 import *


onto = get_ontology("TP9 Ontologies/data/wildlife-en.xml").load()

print("Here are the classes of the ontology:")
print(list(onto.classes()))

print("###\nHere are the instances of each class:")
for cl in onto.classes():
    print(cl.name,cl.instances())
    
print("###\nHere are roles:")
for pr in onto.object_properties():
    print(pr.name,pr.domain,pr.range)
    
print("###\nHere are attributes:")
for da in onto.data_properties():
    print(da.name,da.domain,da.range)
    
print("###\nHere are the individuals and their properties:")
for ind in onto.individuals():
    print(ind)
    for prop in ind.get_properties():
        for value in prop[ind]:
            print(".%s == %s" % (prop.python_name, value))
            
onto.save(file="TP9 Ontologies/data/wildlife-new.owl",format="rdfxml")