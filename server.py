import falcon
import hug
import json
import spacy
import urllib.parse

nlp = spacy.load('en')

hug.API(__name__).http.output_format = hug.output_format.text

##OK
@hug.not_found()
def not_found():
    """URL not found."""
    return {"error": "Not Found"}

@hug.get('/tokenize')
def tokenize(text:hug.types.text='', response=None):
    """Get text tokenizer."""
    if text == '':
        response.status = falcon.HTTP_400
        return {"error": "Text is required."}
    text = urllib.parse.unquote(text)
    data = {}
    data['tokens'] = []
    doc = nlp(text)
    for token in doc:
        data['tokens'].append(token.text)
    return json.dumps(data)

@hug.get('/entities')
def entities(text:hug.types.text='', response=None):
    """get Entity name from sentence."""
    if text == '':
        response.status = falcon.HTTP_400
        return {"error": "Text is required."}
    text = urllib.parse.unquote(text)
    data = {}
    data['entities'] = []
    doc = nlp(text)
    for ent in doc.ents:
        data['entities'].append({
            'text': ent.text,
            'start_char': str(ent.start_char),
            'end_char': str(ent.end_char),
            'label': ent.label_
        })
    return json.dumps(data)

@hug.get('/chunks')
def chunks(text:hug.types.text='', response=None):
    """get chunks nouns from sentence."""
    if text == '':
        response.status = falcon.HTTP_400
        return {"error": "Text is required."}
    text = urllib.parse.unquote(text)
    data = {}
    data['chunks'] = []
    doc = nlp(text)
    for chunk in doc.noun_chunks:
        data['chunks'].append({
            'text': chunk.text,
            'label': chunk.label_
        })
    return json.dumps(data)

@hug.get('/dependencies')
def dependencies(text:hug.types.text='', response=None):
    """get dependencies from sentence."""
    if text == '':
        response.status = falcon.HTTP_400
        return {"error": "Text is required."}
    text = urllib.parse.unquote(text)
    data = {}
    data['dependencies'] = []
    doc = nlp(text)
    for token in doc:
        data['dependencies'].append({
            'text': token.text,
            'dep': token.dep_,
            'parent' : token.head.text
        })
    return json.dumps(data)
