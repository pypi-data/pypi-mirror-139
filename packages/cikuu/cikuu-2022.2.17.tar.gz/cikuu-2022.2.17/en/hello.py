#2022.2.17
from en import * 
from en import terms 
from en import verbnet 

doc = spacy.getdoc("The quick fox jumped over the lazy dog.")
spacy_refresh()

terms.attach(doc) 
verbnet.attach(doc)
print(doc.user_data)