#!/usr/bin/env python
# coding: utf-8

# In[ ]:


'''
Function Instruction

search_patent(patent_id, after, before, kind, cpc, inventor,lawyer,assignee) --
    searching patent by requirements. 
    patent_id = id number of patent (int) 
    after = application date starting after yyyy-mm-dd (string, format:'yyyy-mm-dd')
    before = application date before yyyy-mm-dd (string, format:'yyyy-mm-dd')
    kind = patent kind (A/B1/B2) 
    cpc = cpc section (string)
    inventor, lawyer, assignee = names (string)
    
    Any of above fields could be empty.
    
Example: search_patent(None, '1980-10-1', None, 'B2', 'G', 'Joseph', None, None)

'''


# In[46]:


import pandas as pd
import numpy as np
from datetime import datetime
from functools import partial


# In[6]:


dfk = pd.read_csv("recommender/Data/all_combined.csv").drop(['Unnamed: 0'], axis=1)
inv = pd.read_csv("recommender/Data/inv_cleaned.csv").drop(['Unnamed: 0'], axis=1)
law = pd.read_csv("recommender/Data/law_cleaned.csv").drop(['Unnamed: 0'], axis=1)
asi = pd.read_csv("recommender/Data/asi_cleaned.csv").drop(['Unnamed: 0'], axis=1)


# In[92]:


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

