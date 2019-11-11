from gensim.models.doc2vec import Doc2Vec


def doc2vec(pargraphs, item_type):
    assert item_type in ['title', 'content']
    vector_size = 50 if item_type == 'content' else 10
    window = 4 if item_type == 'content' else 2
    model = Doc2Vec(pargraphs, vector_size=vector_size, window=window, workers=8)

