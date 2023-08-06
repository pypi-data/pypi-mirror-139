import math
import numpy as np
from scipy.spatial import distance

def Cosine_Similarity(vec1, vec2) :
    return 1 - distance.cosine(vec1,vec2)

def Euclidean_Distance(vec1, vec2):
    return distance.euclidean(vec1,vec2)

def Theta(vec1, vec2):
    return math.acos(Cosine_Similarity(vec1,vec2)) + math.radians(10)

def Triangle_Similarity(vec1, vec2):
    theta = math.radians(Theta(vec1,vec2))
    return (np.linalg.norm(vec1) * np.linalg.norm(vec2) * math.sin(theta)) / 2

def Magnitude_Difference(vec1, vec2):
    return abs(np.linalg.norm(vec1) - np.linalg.norm(vec2))

def Sector_Similarity(vec1, vec2):
    ED = Euclidean_Distance(vec1, vec2)
    MD = Magnitude_Difference(vec1, vec2)
    theta = Theta(vec1, vec2)
    return math.pi * math.pow((ED+MD),2) * theta/360

def TS_SS(vec1, vec2):
    return Triangle_Similarity(vec1, vec2) * Sector_Similarity(vec1, vec2)

def pair_wise(lst1,lst2,flag):
    pair_sim = np.zeros((len(lst1),len(lst2)))
    for i in range(pair_sim.shape[0]):
        for j in range(pair_sim.shape[1]):
            if flag == 0:
                pair_sim[i][j] = Cosine_Similarity(lst1[i],lst2[j])
            if flag == 1:
                pair_sim[i][j] = Euclidean_Distance(lst1[i],lst2[j])
            if flag == 2:
                pair_sim[i][j] = TS_SS(lst1[i],lst2[j])
    return pair_sim

def Pairwise_Cosine_Similarity(lst1,lst2):
    return pair_wise(lst1,lst2,0)

def Pairwise_Euclidean_Distance(lst1,lst2):
    return pair_wise(lst1,lst2,1)
    
def Pairwise_TS_SS(lst1,lst2):
    return pair_wise(lst1,lst2,2)

