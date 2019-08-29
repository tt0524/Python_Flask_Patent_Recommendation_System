import pandas as pd
import numpy as np
import scipy.sparse
from scipy.sparse import csr_matrix

patent_sample = pd.read_csv('recommender/Data/all_combined.csv').drop(['Unnamed: 0'], axis=1)
patent_index = pd.read_csv('recommender/Data/citation_patent_index_mapping.csv').drop(['Unnamed: 0'], axis=1)
patent_index.patent_id = patent_index.patent_id.astype(str)

citation_matrix = scipy.sparse.load_npz('recommender/Data/citation_sparse_matrix.npz')

def pairwise_jaccard(X):
    """Computes the Jaccard distance between the rows of `X`.
    """
    X = X.astype(bool).astype(int)

    intrsct = X.dot(X.T)
    row_sums = intrsct.diagonal()
    unions = row_sums[:,None] + row_sums - intrsct
    sims = intrsct / unions
    n = X.shape[0]
    for i in range(n):
        sims[i,i] = 0.0
    return sims

def get_neighbors(patent_id, sims, patent_index):
    """

    """
    if patent_id not in list(patent_index.patent_id):
        return []
    index = patent_index[patent_index.patent_id == patent_id].iloc[0]['patent_index']
    neighbors = [(i,j) for (i,j) in enumerate(sims[index].tolist()[0]) if j > 0.0]
    neighbors.sort(key=lambda x: x[1], reverse=True)
    recomm_list = [ patent_index[patent_index.patent_index == index].iloc[0]['patent_id'] for (index, sim) in neighbors]
    return recomm_list

def search_similar_item_citation(patent_id):
    """
    get the result dataframe
    """
    if patent_id not in list(patent_index.patent_id):
        return pd.DataFrame()
    sims = pairwise_jaccard(citation_matrix)
    idlist = get_neighbors(patent_id, sims, patent_index)
    temp = patent_sample.copy()
    temp = temp[temp['id'].isin(idlist)]
    return temp


# patent_id = '3943599'
# temp = search_similar_item_citation(patent_id)
# print(temp)