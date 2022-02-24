import math
import copy
import sys

class coord():
    
    def __init__(self, name,x,y) -> None:
        self.name = name
        self.x = x
        self.y = y
    
    def euclid(self, c):
        return math.sqrt((self.x-c.x)**2 + (self.y-c.y)**2)

def hierarchical_one_pass_single(clusters):
    cluster_mins = []
    for k1, v1 in clusters.items():
        m = 10000000.0
        for k2, v2 in clusters.items():
            if k1 == k2:
                continue
            for p1 in clusters[k1]:
                for p2 in clusters[k2]:
                    curr = p1.euclid(p2)
                    if curr < m:
                        m = curr
                        clus = [k1,k2]
                        

        cluster_mins.append((copy.deepcopy(m),copy.deepcopy(clus)))
    #https://stackoverflow.com/questions/14802128/tuple-pairs-finding-minimum-using-python
    min_entry=min(cluster_mins, key=lambda t:t[0])

    new_cluster_name = "".join(min_entry[1])
    new_cluster_entries = []
    print(f"Single link clusters to join= {min_entry[1]} | distance={min_entry[0]}")
    for c_name in min_entry[1]:
        new_cluster_entries[:]+=copy.deepcopy(clusters[c_name])
        del clusters[c_name]
    clusters[new_cluster_name]=new_cluster_entries
    return clusters

def hierarchical_one_pass_complete(clusters):
    cluster_mins = []
    min_cluster = 10000.0
    for k1, v1 in clusters.items():
        point_max = []
        pair_max = []
        for k2, v2 in clusters.items():
            if k1 == k2:
                continue
            #loop through the points of the main cluster
            curr_max = 0.0
            for p1 in clusters[k1]:
                #loop through the points of the cluster comparing to
                for p2 in clusters[k2]:
                    distance =p1.euclid(p2)
                    if distance > curr_max:
                        curr_max = distance
            
            point_max.append(copy.deepcopy(curr_max))
            pair_max.append([k1,k2])          

        cluster_mins.append((min(point_max),pair_max[point_max.index(min(point_max))]))

    #https://stackoverflow.com/questions/14802128/tuple-pairs-finding-minimum-using-python
    min_entry=min(cluster_mins, key=lambda t:t[0])
    print(f"Complete link clusters to join= {min_entry[1]} | distance={min_entry[0]}")
    new_cluster_name = "".join(min_entry[1])
    new_cluster_entries = []
    for c_name in min_entry[1]:
        new_cluster_entries[:]+=copy.deepcopy(clusters[c_name])
        del clusters[c_name]
    clusters[new_cluster_name]=new_cluster_entries
    return clusters 

A = coord('A',1,6)
B= coord('B',1002,20)
C = coord('C',498,651)
D = coord('D',6,10)
E = coord('E',510,622)
F = coord('F',503,632)
G = coord('G',4,9)
H= coord('H',1010,25)
I = coord('I',1006,30)
J = coord('J',502,680)    

points = [A,B,C,D,E,F,G,H,I,J]
clusters = {c.name:[c] for c in points}
new_clusters = copy.deepcopy(clusters)

while len(new_clusters.keys())>3:
    new_clusters = hierarchical_one_pass_single(new_clusters)

while len(clusters.keys())>3:
    clusters = hierarchical_one_pass_complete(clusters)
print("\n")

print("Single Link Cluster Results: "),
for k in new_clusters.keys():
    print(f"{k}"),

print("Complete Link Cluster Results: "),
for k in clusters.keys():
    print(f"{k}"),
print("\n")