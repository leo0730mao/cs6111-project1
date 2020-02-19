from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))
idf_global = dict()
tf_global = dict()

# tokenize, stem, remove stop words
def preprocess_doc(document):
    words = word_tokenize(document)
    terms = [stemmer.stem(w) for w in words if not stemmer.stem(w) in stop_words]
    return terms

def terms_to_vector(document, id):
    ''' process a document represented as a list of terms
    to tf vector and populate idf dictionary
    '''
    tf = dict()
    for term in document:
        if not term in tf:
            tf[term] = 0
        tf[term] += 1
        if not term in idf:
            idf[term] = dict()
        if not id in idf[term]:
            idf[term][id] = 0
        idf[term][id] += 1
    return tf

def get_document_list(documents):
    """ Given a list of documents and whether they are relevant,
    generate a document list in the structure to be processed by
    query update function
    
    Parameters
    ----------
    documents : map
        map of doc ids to snippets (strings) documents to isRelevant (bool) returned by google search engine processed by main
    
    Returns
    -------
    
    """
    documentList = dict()
    for doc in documents:
        terms = preprocess_doc(doc)
        documentList[doc] = dict()
        documentList[doc]["snippets"] = terms
        documentList[doc]["isRelevant"] = doc["isRelevant"]
        documentList[doc]["tfvec"] = terms_to_vector(terms)
    
    return documentList
        
        
def calculate_term_weights(alpha = 1.0, beta = 0.75, gamma = 0.15, query_weights, documentList):
    
    #q = preprocess_doc(q)
    weights = dict()
    for term in idf:
        weights[term] = 0.0
    
    relTFWeights = dict()
    nonRelTFWeights = dict()
    relCount = 0
    nonRelCount = 0
    
    candidate_weights = dict()
    
    for id in documentList:
        doc = documentList[id]
        if doc["isRelevant"] is True:
            relCount += 1
            for term in doc["tfvec"]:
                relTFWeights[term] = doc["tfvec"][term] if not term in relTFWeights else relTFWeights[term] + doc["tfvec"][term]
        else:
            nonRelCount += 1
            for term in doc["tfvec"]:
                nonRelTFWeights[term] = doc["tfvec"][term] if not term in nonRelTFWeights else nonRelTFWeights[term] + doc["tfvec"][term]
    
#    for id in relDocs:
#        doc = documentList[id]
#        for term in doc["tfvec"]:
#            relTFWeights[term] = doc["tfvec"][term] if not term in relTFWeights else relTFWeights[term] + doc["tfvec"][term]
#
#    for id in nonRelDocs:
#        doc = documentList[id]
#        for term in doc["tfvec"]:
#            nonRelTFWeights[term] = doc["tfvec"][term] if no term in nonRelTFWeights else nonRelTFWeights[term] + doc["tfvec"][term]
    
    # use t: log of idf
    for term in idf_global:
        idf = Math.log(len(documents) / len(idf_global[term]), 10)
    
        for doc in idf_global[term]:
            if doc["isRelevant"] is True:
                weights[term] += beta * idf * (relTFWeights["term"] / relCount)
            else:
                weights[term] -= gamma * idf * (nonRelTFWeights["term"] / nonRelCount)
        if term in query_weights:
            query_weights[term] += alpha * query_weights[term] + weights[term]
        else:
            if term in candidate_weights:
                candidate_weights[term] += weights[term]
            else:
                candidate_weights[term] = weights[term]
        
    # find out the two terms with most weight
    max_val = 0
    second_val = 0
    first = None
    second = None
    for candidate, val in candidate_weights.values():
        if val > max_val:
            second = first
            second_val = max_val
            first = candidate
            max_val = val
        elif val > second_val:
            second_val = val
            second = candidate
    query_weights[first] = max_val
    query_weights[second] = second_val
    return query_weights.keys()
            
                
    
    
