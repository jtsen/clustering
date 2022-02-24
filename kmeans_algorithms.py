import copy, sys

class coord():
    """
    Class to store a single record.
    This object can interact with other objects of the same type by calculating their distances
    in squared euclidian or manhattan distance. Can also check equivalence.
    """
    #variadic constructor that takes in variable numbers of keyword arguments
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    #euclidian squared calculation
    def euclid(self, c):
        summation = 0
        for (k,v), (k1,v1) in zip(self.__dict__.items(),c.__dict__.items()):
            #skip the name
            if type(v) is str:
                break
            summation += (v-v1)**2
        return summation
    
    #manhattan distance calculation
    def manh(self, c):
        summation = 0
        for (k,v), (k1,v1) in zip(self.__dict__.items(),c.__dict__.items()):
            #skip the name
            if type(v) is str:
                break
            summation += abs(v-v1)
        return summation

    #check equivalence of all instance key-value variables
    def equi(self, c):
        for (k,v), (k1,v1) in zip(self.__dict__.items(),c.__dict__.items()):
            if v != v1:
                return False
        return True
    #print the record / centroid as per lab spec
    def print_coords(self, c=False):
        coord = []
        for k,v in self.__dict__.items():
            if type(v) is str:
                break
            coord.append(v)
        if c:
            print(" Centroid: ", end=' '),
        for val in coord:
            print(val, end=' ')
        print("\n")
            
def read_input(path):
    """
    Read in comma separated text file line-by-line
    while indexing each predictive attribute alphabetically.
    The last item of the line is treated as the label of 
    that specific record. 

    Args:
        path ([str]): [relative or absolute path to the input file]

    Returns:
        data [list[Coords]]: [a list containing of all of the records in the input file]
        keys [list[str]]: [a list (set) containing all of the colume name]
    """
    data = []
    with open(path) as input_file:
        line = input_file.readline()
        # while the current line exists
        while line:
            #remove newline character and split the string into a list of strings on commas
            curr = line.replace("\n","").split(",")
            #cast predictive attributes into floats
            for i in range(len(curr)-1):
                curr[i] = float(curr[i])
            #build a key list starting from a (unicode)
            keys = [chr(ord('`')+1+i) for i in range(len(curr)-1)]
            keys.append('name')
            #build a dictionary with the key list and the list of attributes
            coordinate = dict(zip(keys,curr))
            #intialize Coord object for current record with the dictionary built
            curr_coord = coord(**coordinate)
            #append this Coord to list for return
            data.append(copy.deepcopy(curr_coord))
            #read the next line
            line = input_file.readline()
    
    return data, keys

def parse_centroid(centroids):
    """
    Parses command line inputed centroids
    in the following format: 0,0 200,200 140,140
    in n-dimensions. Basically read_input for centroids.

    Args:
        centroids ([list[str]]): [list of strings representing the predictive attribute columns of the centroid]

    Returns:
        final [list[Coord]]: [list of centorids as Coord objects]
    """
    final = []
    #enumerate all the entries in the dictionary
    for index, c in enumerate(centroids):
        #split the columns
        c_list = c.split(",")
        #add a cluster name to the list of attributes
        c_list.append("C"+str(index+1))
        #cast each column entry into float
        for i in range(len(c_list)-1):
            c_list[i] = float(c_list[i])
        keys = [chr(ord('`')+1+i) for i in range(len(c_list)-1)]
        keys.append('name')
        centroids_parsed = dict(zip(keys,c_list))
        curr_coord = coord(**centroids_parsed)
        final.append(copy.deepcopy(curr_coord))
    
    return final

def kmeans_solver(input_file, centroid, distance='e2'):
    """
    K-Means algorithm.

    Args:
        input_file ([str]): [relative or absolute path of input file]
        centroid ([list[str]]): [a list of strings that are comma separated strings]
        distance (str, optional): [distance function e2/manh]. Defaults to 'e2'.

    Returns:
       clusters [dict]: [resulting clusters]
       centroids [dict]: [resulting centroids]
    """
    #centroids are lists of coordinates Strings to start
    #parse them into libraries with names
    cent = parse_centroid(centroid)

    centroids={c.name:c for c in cent}
    old_centroids=copy.deepcopy(centroids)

    #read the input file 
    data, keys = read_input(input_file)

    #make sure the centroids have the same dimension
    if len(keys) != len(cent[0].__dict__.keys()):
        sys.exit("Error: Centroid dimension not equal to Input dimension")
    
    #start of algorithm
    #initialize clusters
    clusters={c.name:[] for c in cent}

    #Loop until convergence
    while True:
        clusters={c.name:[] for c in cent}

        #loop through the coordinates
        for coordinate in data:
            #list for storing the distances of a coordinate to all the centroids
            dist_to_clusters = []
            cluster_dist_index = []
            #loop through the centroids for each coordinate
            for c, value in centroids.items():
                #calculate and add the distance between the current coordinate and current iteration centroids
                if distance == 'e2':
                    dist_to_clusters.append(coordinate.euclid(value))
                elif distance == 'manh':
                    dist_to_clusters.append(coordinate.manh(value))
                cluster_dist_index.append(c)
            clusters[cluster_dist_index[dist_to_clusters.index(min(dist_to_clusters))]].append(coordinate)
        #recompute the centroids according to the new clusters
        for cluster,coords in clusters.items():
            #if no data points are added to the cluster associated with this centroid, skip it and preserve original centroid value
            if not coords:
                continue
            #otherwise, update the centroid to the mean of the coordinates of the points in the cluster
            for k,v in coords[0].__dict__.items():
                if k == 'name':
                    continue
                running_sum=0.0
                for point in coords:
                    if type(point.__dict__.get(k)) is str:
                        continue
                    running_sum+=float(point.__dict__.get(k))
                centroids[cluster].__dict__.update({k:copy.deepcopy(running_sum/len(coords))})
        for k,v in clusters.items():
            print(k, end=' '),
            print(' -> ', end=' ')
            for i in v:
                print(i.name, end=' ')
            print("\n")
        for k,v in centroids.items():
            v.print_coords(c=True)

        #break here if old = new clusters -> which means centroids of clusters did not change
        #reference: https://stackoverflow.com/questions/20736709/how-to-iterate-over-two-dictionaries-at-once-and-get-a-result-using-values-and-k
        if all(v.equi(v2) for (k,v), (k2,v2) in zip(centroids.items(), old_centroids.items())):
            break
            
        #set old centroids for comparison after the next iteration
        old_centroids=copy.deepcopy(centroids)
    
    #print the cluster results and the final centroid values as per lab spec
    for k,v in clusters.items():
        print(k, end=' '),
        print(' -> ', end=' ')
        for i in v:
            print(i.name, end=' ')
        print("\n")
    for k,v in centroids.items():
        v.print_coords(c=True)

    return clusters, centroids