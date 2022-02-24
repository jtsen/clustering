import copy
from kmeans_algorithms import coord

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
        labels [list[str]]: [a list (set) containing all of the unique attributes]
        labels_in_order [list[labels]]: [a list containing all the labels in the order of the file]
    """
    data = []
    with open(path) as input_file:
        #initialise by reading first line
        line = input_file.readline()
        #initialize lists to return
        labels =[]
        labels_in_order=[]
        #loop while the current line exists
        while line:
            #replace newline character and splie the str into a list of str on commas
            curr = line.replace("\n","").split(",")
            #cast the predictive attributes into floats
            for i in range(len(curr)-1):
                curr[i] = float(curr[i])
            #build a key list starting from a (unicode)
            keys = [chr(ord('`')+1+i) for i in range(len(curr)-1)]
            #last item is the label
            keys.append('label')
            #build a dictionary from the current line and the key list
            coordinate = dict(zip(keys,curr))
            #find all unique labels and store them in list to return
            if coordinate['label'] not in labels:
                labels.append(coordinate['label'])
            #add current line's label in list to return
            labels_in_order.append(coordinate['label'])
            #initialize Coord object with dictionary built in line 38 (varargs)
            curr_coord = coord(**coordinate)
            #add the current record to the list to return
            data.append(copy.deepcopy(curr_coord))
            #read the next line
            line = input_file.readline()
    
    return data, labels, labels_in_order

def kNN(train, test, k=3, distance='e2', uw=False):
    """
    K-nearest-neighbor algorithm. 

    Args:
        train ([list[Coords]]): [training dataset]
        test ([list[Coords]]): [test dataset]
        k (int, optional): [number of neighbors to consider]. Defaults to 3.
        distance (str, optional): [distance function: e2/manh]. Defaults to 'e2'.
        uw (bool, optional): [whether or not to use unit voting weights]. Defaults to False.

    Returns:
        res [list[str]]: [classification attribute of records in sequential order]
        test_labels_ordered [list[str]]: [real classification attribute of records in sequential order]
        results [dict{dict}]: [True positives and false negatives of each attribute]
    """
    #read training and test set
    train, train_labels, train_labels_ordered = read_input(train)
    test, test_labels, test_labels_ordered = read_input(test)
    #initialize result list to return
    res = []
    #iterate over all records in the test set
    for test_coord in test:
        #initialize intermediate storage for distances for the current record
        distance = []
        #calculate the distance of the current test row 
        for index, train_coord in enumerate(train):
            if distance == 'manh':
                distance.append((index, test_coord.manh(train_coord)))
            distance.append((index, test_coord.euclid(train_coord)))
        #sort the distances to all the records in the training set in increasing order    
        distance.sort(key=lambda distance:distance[1])
        #take the k-nearest-neighbor
        distance=distance[0:k]
        #initialize and populate labels count dictionary with predictive attribute column keys
        label_count = {x:0.0 for x in train_labels}
        #iterate for the k neighbors we've chosen
        for neighbor in distance:
            #whether use unit voting weights or 1/max(d,0.0001)
            if uw:
                # 0 is index, 1 is distance
                label_count[train[neighbor[0]].label] += 1
            else:
                label_count[train[neighbor[0]].label] += 1/max(neighbor[1],0.0001)
        #append the resulting label with max votes
        res.append(max(label_count, key=label_count.get))
    #intialize results dictionary to return tp/fn    
    results = {x:{'tp':0, 'fn':0} for x in train_labels}
    #count of total amount of each classfication attribute
    attr_counts = {x:0 for x in train_labels}
    #print the results to standard output as lab spec
    for i, j in zip(res,test_labels_ordered):
        print(f"want={j} got={i}")
        if i == j:
            results[i]['tp']+=1
        elif i != j:
            results[i]['fn']+=1
        attr_counts[j]+=1
    #print the recall and precision to standard output as lab spec
    for key,value in sorted(results.items()):
        print(f"Label={key} Precision={value['tp']}/{value['tp']+value['fn']} Recall={value['tp']}/{attr_counts[key]}")
    

    return res, test_labels_ordered, results