import argparse, knn_algorithms

if __name__ == '__main__':
    """
    Driver function for parsing commandline input and invoking
    the specified algorithms and parameters
    """
    
    #create the argparse parser object
    parser = argparse.ArgumentParser()
    parser.add_argument("-k",
                        dest="k",
                        default=3,
                        type=int,
                        help="number of neighbors; default=3")
    parser.add_argument("-d",
                        dest="distance",
                        default="e2",
                        help="distance measure; manh/e2; default=e2")
    parser.add_argument("-unitw",
                        dest="unitw",
                        action="store_true",
                        default=False,
                        help="unit voting weights flag; defaults to 1/d")
    parser.add_argument("-train",
                        required=True,
                        dest="train_file",
                        help="training file")
    parser.add_argument("-test",
                        required=True,
                        dest="test_file",
                        help="testing file")
    
    args = parser.parse_args()
    
    results, test_labels, res_counts = knn_algorithms.kNN(args.train_file, args.test_file, distance=args.distance, k=args.k, uw=args.unitw)