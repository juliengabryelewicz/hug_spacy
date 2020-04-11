import hug
import server
from falcon import HTTP_200, HTTP_400, HTTP_404

def test_not_found():
    response = hug.test.get(server, '', {})
    assert response.status == HTTP_404

def test_parse_without_params():
    response = hug.test.get(server, '/tokenize', {})
    assert response.status == HTTP_400

def test_with_empty_param():
    response = hug.test.get(server, '/tokenize', {'text': ''})
    assert response.status == HTTP_400

def test_tokenizer():
    response = hug.test.get(server, '/tokenize', {'text': 'text is required'})
    assert response.status == HTTP_200
    assert response.data == '{"tokens": ["text", "is", "required"]}'

def test_entities():
    response = hug.test.get(server, '/entities', {'text': 'apple is a company'})
    assert response.status == HTTP_200
    assert response.data == '{"entities": [{"text": "apple", "start_char": "0", "end_char": "5", "label": "ORG"}]}'

def test_chunks():
    response = hug.test.get(server, '/chunks', {'text': 'apple is a company'})
    assert response.status == HTTP_200
    assert response.data == '{"chunks": [{"text": "apple", "label": "NP"}, {"text": "a company", "label": "NP"}]}'

def test_dependencies():
    response = hug.test.get(server, '/dependencies', {'text': 'apple is a company'})
    assert response.status == HTTP_200
    assert response.data == '{"dependencies": [{"text": "apple", "dep": "nsubj", "parent": "is"}, {"text": "is", "dep": "ROOT", "parent": "is"}, {"text": "a", "dep": "det", "parent": "company"}, {"text": "company", "dep": "attr", "parent": "is"}]}'
