#!/usr/bin/env python
# coding: utf-8

# In[21]:


'''
Function Instruction

hybrid_pipe(patent_id, after, before, kind, cpc, inventor,lawyer,assignee,sentence) --
    searching patent by requirements. 
    patent_id = id number of patent (int) 
    after = application date starting after yyyy-mm-dd (string, format:'yyyy-mm-dd')
    before = application date before yyyy-mm-dd (string, format:'yyyy-mm-dd')
    kind = patent kind (A/B1/B2) 
    cpc = cpc section (string)
    inventor, lawyer, assignee = names (string)
    sentence = keywords (string)
    
    Any of above fields could be empty.
    
Example: hybrid_pipe(None, None , None, 'B2', 'A', None, None, None, 'molecule')

'''


# In[25]:


import pandas as pd
import numpy as np
from datetime import datetime
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# In[26]:


dfk = pd.read_csv("recommender/Data/all_combined.csv").drop(['Unnamed: 0'], axis=1)
inv = pd.read_csv("recommender/Data/inv_cleaned.csv").drop(['Unnamed: 0'], axis=1)
law = pd.read_csv("recommender/Data/law_cleaned.csv").drop(['Unnamed: 0'], axis=1)
asi = pd.read_csv("recommender/Data/asi_cleaned.csv").drop(['Unnamed: 0'], axis=1)

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

sim_t = cosine_similarity(dftx)
sim_a = cosine_similarity(dftx1)
word_list_title = dftx.columns.get_values().tolist()
word_list_abstract = dftx1.columns.get_values().tolist()


# In[27]:


def search_id(id):
    if id == None:
        temp = dfk.copy()
        return temp
    else:
        temp = dfk[(dfk['number'] == id)]
        return temp

def search_kind(kind):
    if kind == None:
        temp = dfk.copy()
        return temp
    else:
        temp = dfk[(dfk['kind'] == kind)]
        return temp

def search_cpc(cpc):
    if cpc == None:
        temp = dfk.copy()
    else:
        temp = dfk[(dfk[cpc] == 1.0)]
        
    return temp

def search_date(after, before):
    temp = dfk.copy()
    temp['date'] = pd.to_datetime(temp['date']).astype(int)/ 10**9
    
    if(before == None):
        mid = temp.copy()
    else:
        before = datetime.strptime(before, '%Y-%m-%d')
        before = before.timestamp()
        mid = temp[(temp['date'] < before)]
        
    if(after == None):
        res = mid.copy()
    else:
        after = datetime.strptime(after, '%Y-%m-%d')
        after = after.timestamp()
        res = mid[(mid['date'] > after)]
    
    return res

def search_class(patent_id, after, before, kind, cpc):
    id_search = search_id(patent_id)['id'].tolist()
    date_search = search_date(after, before)['id'].tolist()
    kind_search = search_kind(kind)['id'].tolist()
    cpc_search = search_cpc(cpc)['id'].tolist()
    
    res = list(set(id_search)&set(date_search)&set(kind_search)&set(cpc_search))
    return res

def search_inv(inventor):
    if inventor == None:
        temp = inv.copy()
        return temp
    else:
        temp_f = inv[inv['name_first'].str.contains(inventor, na = False, case=False)] #Ignore case and None value
        temp_l = inv[inv['name_last'].str.contains(inventor, na = False, case=False)]
        temp_id = inv[inv['inventor_id'].str.contains(inventor, na = False, case=False)]
        frames = [temp_f, temp_l,temp_id]
        temp = pd.concat(frames)
        temp = temp.drop_duplicates()
        return temp

def search_law(lawyer):
    if lawyer == None:
        temp = law.copy()
        return temp
    else:
        temp_f = law[law['name_first'].str.contains(lawyer, na = False, case=False)] #Ignore case and None value
        temp_l = law[law['name_last'].str.contains(lawyer, na = False, case=False)]
        temp_o = law[law['organization'].str.contains(lawyer, na = False, case=False)]
        temp_id = law[law['lawyer_id'].str.contains(lawyer, na = False, case=False)]
        frames = [temp_f, temp_l, temp_o, temp_id]
        temp = pd.concat(frames)
        temp = temp.drop_duplicates()
        return temp

def search_asi(assignee):
    if assignee == None:
        temp = asi.copy()
        return temp
    else:
        temp_f = asi[asi['name_first'].str.contains(assignee, na = False, case=False)] #Ignore case and None value
        temp_l = asi[asi['name_last'].str.contains(assignee, na = False, case=False)]
        temp_o = asi[asi['organization'].str.contains(assignee, na = False, case=False)]
        temp_id = asi[asi['assignee_id'].str.contains(assignee, na = False, case=False)]
        frames = [temp_f, temp_l, temp_o, temp_id]
        temp = pd.concat(frames)
        temp = temp.drop_duplicates()
        return temp

def search_by_name(inventor,lawyer,assignee):
    temp_i = search_inv(inventor)
    i = temp_i['patent_id'].tolist()
    temp_l = search_law(lawyer)
    l = temp_l['patent_id'].tolist()
    temp_a = search_asi(assignee)
    a = temp_a['patent_id'].tolist()
    
    res = list(set(i)&set(l)&set(a))
    return res

def find_by_id(idlist):
    temp = dfk.copy()
    temp['id'] = temp['id']
    temp = temp[temp['id'].isin(idlist)]
    return temp

def search_patent(patent_id, after, before, kind, cpc, inventor,lawyer,assignee):
    res_1 = search_class(patent_id, after, before, kind, cpc)
    res_2 = search_by_name(inventor,lawyer,assignee)
    res = list(set(res_1)&set(res_2))
    
    temp = find_by_id(res)
    return temp

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


# In[50]:


def hybrid_pipe(patent_id, after, before, kind, cpc, inventor,lawyer,assignee,sentence):
    cascade = search_patent(patent_id, after, before, kind, cpc, inventor,lawyer,assignee)
    res_0 = cascade['id'].tolist()
    if sentence == None:
        res = cascade.copy()
    else:
        res_m = cascade.copy()
        wordlist = re.sub("[^\w]", " ", sentence).split()
        temp = pd.DataFrame()
        for i in range(len(wordlist)):
            temp[wordlist[i]] = tfidf_weighted(wordlist[i])['result_weighted']

        temp.loc[:, 'Total'] = temp.sum(axis=1)
        temp = temp[['Total']]

        # res = temp.sort_values(by="Total" , ascending=False)
        res = pd.concat([res_m, temp], axis=1).sort_values(by="Total", ascending=False)
        res = res.dropna(subset=['title'])
        res = res[(res['Total'] > 0)]
    
    return res
    

