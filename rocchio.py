import numpy as np
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer


def get_doc(web_page):
    stemmer = PorterStemmer()
    stop_words = set(stopwords.words('english'))

    doc = web_page['title'] + " " + web_page['snippet']
    words = word_tokenize(doc)
    # terms = [stemmer.stem(w) for w in words if not stemmer.stem(w) in stop_words]
    terms = [w.lower() for w in words if w not in stop_words]
    return " ".join(terms)


def doc_vector(query, relevant, non_relevant):
    corpus = [query] + relevant + non_relevant
    r_len = len(relevant)

    tf_idf_model = TfidfVectorizer().fit(corpus)
    tf_idf_m = tf_idf_model.transform(corpus).todense()

    q_vector = tf_idf_m[0]
    r_vector = tf_idf_m[1: r_len + 1]
    n_vector = tf_idf_m[r_len + 1:]
    return q_vector, r_vector, n_vector, tf_idf_model.get_feature_names()


def rocchio(query, relevant, non_relevant):
    if len(relevant) == 0:
        print("not enough information")
        return query, False
    tmp_query = query.lower()
    relevant = [get_doc(d) for d in relevant]
    non_relevant = [get_doc(d) for d in non_relevant]

    beta = 0.75
    gamma = 0.15

    print("indexing...")
    q_vector, r_vector, n_vector, vocabulary = doc_vector(tmp_query, relevant, non_relevant)
    r_vector = r_vector.sum(axis = 0)
    n_vector = n_vector.sum(axis = 0)

    rocchio_vector = beta * r_vector / len(relevant) - gamma * n_vector / len(non_relevant)
    rocchio_vector[rocchio_vector < 0] = 0

    new_q = q_vector + rocchio_vector
    index = new_q.argsort()
    index = np.flip(index).tolist()[0]

    count = 0
    tmp = set(tmp_query.split(" "))
    augment_words = []
    for i in index:
        if vocabulary[i] not in tmp:
            augment_words.append(vocabulary[i])
            count += 1
        if count >= 2:
            break
    print("augment with words: " + " ".join(augment_words))
    return query + " " + " ".join(augment_words), True





