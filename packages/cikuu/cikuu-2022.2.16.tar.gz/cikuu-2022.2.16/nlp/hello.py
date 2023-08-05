#2022.2.14
from nlp import * 
from nlp import terms 
from nlp import verbnet 

doc = spacy.getdoc("The quick fox jumped over the lazy dog.")
spacy_refresh()

terms.attach(doc) 
verbnet.attach(doc)
print(doc.user_data)