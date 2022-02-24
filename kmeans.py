import argparse, sys
import kmeans_algorithms

if __name__ == '__main__':
    """
    K-Means Driver function for parsing commandline input and invoking
    the specified algorithms and parameters
    """
    
    #create the argparse parser object
    parser = argparse.ArgumentParser()
    parser.add_argument("-d",
                        dest="distance",
                        default="e2",
                        help="distance measure; manh/e2; default=e2")
    parser.add_argument("-data",
                        required=True,
                        dest="input_file",
                        help="input file to cluster")
    parser.add_argument('centroids',
                         nargs='*')
    
    
    args = parser.parse_args()
    
    if len(args.centroids)<2:
        sys.exit('Error! Please input centroids')
    
    clusters, centroids =kmeans_algorithms.kmeans_solver(args.input_file, args.centroids, args.distance)

