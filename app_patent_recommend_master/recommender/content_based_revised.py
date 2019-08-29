#!/usr/bin/env python
# coding: utf-8

# In[91]:


'''
Instructions of functions:

tfidf_weighted_words(sentence) -- calculating tf-idf scores for an assigned word or a sentence. 
    Example: tfidf_weighted_words('bicycle')
             tfidf_weighted_words('big data analysis')
             
tfidf_similarity(patent_id) -- calculating the similarity for a patent. Input should be a patent id number. 
    Example: tfidf_similarity(10000000)

'''


# In[15]:


import pandas as pd
import numpy as np
import re
import nltk
# nltk.download()

from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[16]:



df = pd.read_csv("recommender/Data/all_combined.csv").drop(['Unnamed: 0'], axis=1)
dft = df.copy()
stop = stopwords.words('english')

dft['title'] = dft['title'].str.lower()
dft['title'] = dft['title'].str.replace('\d+', '')
dft['title'] = dft['title'].str.split(' ').apply(lambda x: [item for item in x if item not in stop])
dft['title']=dft['title'].apply(', '.join)
v = TfidfVectorizer()
x = v.fit_transform(dft['title'])
dftx = pd.DataFrame(x.toarray(), columns=v.get_feature_names())
tfidf= pd.concat([df, dftx], axis=1)

dft['abstract'] = dft['abstract'].str.lower()
dft['abstract'] = dft['abstract'].str.replace('\d+', '')
dft['abstract'] = dft['abstract'].str.split(' ').apply(lambda x: [item for item in x if item not in stop])
dft['abstract'] = dft['abstract'].apply(', '.join)
x1 = v.fit_transform(dft['abstract'])
dftx1 = pd.DataFrame(x1.toarray(), columns=v.get_feature_names())
tfidf1= pd.concat([df, dftx1], axis=1)


# In[17]:


sim_t = cosine_similarity(dftx)
sim_a = cosine_similarity(dftx1)
word_list_title = dftx.columns.get_values().tolist()
word_list_abstract = dftx1.columns.get_values().tolist()


# In[18]:


def tfidf_weighted(word):
    temp = df.copy()
    word = word.lower()
    
    if word in word_list_abstract:
        temp_a = tfidf1.sort_values(by=word , ascending=False)[[word]]
        temp['result_a'] = temp_a[[word]]
    else:
        temp['result_a'] = 0.0
        
    if word in word_list_title:
        temp_t = tfidf.sort_values(by=word , ascending=False)[[word]]
        temp['result_t'] = temp_t[[word]]
    else:
        temp['result_t'] = 0.0
    
    temp['result_weighted'] = 0.8 * temp['result_t'] + 0.2 * temp['result_a']
    temp = temp.sort_values(by=['result_weighted'] , ascending=False)
    #temp = temp[(temp['result_weighted'] > 0)]
    temp = temp.drop(columns=['result_t', 'result_a'])
    
    return temp

def tfidf_weighted_words(sentence):
    wordlist = re.sub("[^\w]", " ",  sentence).split()
    temp = pd.DataFrame()
    for i in range(len(wordlist)):
        temp[wordlist[i]] = tfidf_weighted(wordlist[i])['result_weighted']
    
    temp.loc[:,'Total'] = temp.sum(axis=1)
    temp = temp[['Total']]
    
    res = pd.concat([df, temp], axis=1).sort_values(by="Total" , ascending=False)
    res = res[(res['Total'] > 0)]
    return res


# In[19]:


def tfidf_similarity(patent_id):
    temp = df.copy()
    index = temp[temp['id']==patent_id].index.values.astype(int)[0]
    temp['sim_temp_t'] = sim_t[index]
    temp['sim_temp_a'] = sim_a[index]
    temp['sim_temp'] = 0.8 * temp['sim_temp_t'] + 0.2 * temp['sim_temp_a']
    temp = temp.sort_values(by="sim_temp" , ascending=False)
    temp = temp[(temp['sim_temp'] > 0)]
    temp = temp[1:6]
    temp = temp.drop(columns=['sim_temp_t', 'sim_temp_a'])
    
    return temp

if __name__ == '__main__':
    pass

