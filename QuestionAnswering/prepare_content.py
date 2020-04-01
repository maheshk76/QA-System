from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import nltk
from nltk import ne_chunk
nltk.download('stopwords')
from sklearn import feature_extraction as fe
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from nltk import ne_chunk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
cv = CountVectorizer()
tfidf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
#stopWords = set(stopwords.words("english"))
def prepare_content_QA(corpus):
    one_paragraph=""
    total_sentences=[]
    similar_sentences=[]
    cosine_vals_all=[]
    filtered_cosine_vals=[]
    for i in corpus:
        for y in sent_tokenize(i):
            total_sentences.append(y)
    #finding tfidf of sentences,pass the list sentences
    word_count = cv.fit_transform(total_sentences)
    allfeatures_with=tfidf_transformer.fit_transform(word_count)
    #returns numpy array
    cosine_sims_temp=cosine_similarity(allfeatures_with[0:1],allfeatures_with)
    #converting to the list ,numpy array
    for c in cosine_sims_temp:
        for x in c:
            cosine_vals_all.append(x)
    print("Total sentences from wiki:",len(cosine_vals_all))
    for vals in cosine_vals_all:
        #define range and extract most from cosine_sims_list
        if(vals>0.10 and vals<1):
            #creating new lists 
            similar_sentences.append(total_sentences[cosine_vals_all.index(vals)])
            filtered_cosine_vals.append(cosine_vals_all[cosine_vals_all.index(vals)])
    print("Most Similar sentences:",len(similar_sentences))
    for p in similar_sentences:
        one_paragraph+=''.join(p)
    print(one_paragraph)
    return one_paragraph