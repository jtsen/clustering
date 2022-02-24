# K-Means / K-Nearest-Neighbor

## Description
This program consists of a K-Means and a K-Nearest-Neighbor algorithm implemented with Python3 built-in libraries.


## Usage
To compile and run *K-Nearest-Neighbor*:
```bash
python3 path [-k $k] [-d $distance] [-unitw $unitw] -train $train -test $test
```
Example:
```bash
python3 ./knn.py -train some-input.txt -test test-file.txt
python3 ./knn.py 3 -d manh -train some-input.txt -test test-file.txt
python3 ./knn.py 3 -d manh -train some-input.txt -test test-file.txt -unitw
```

Where:
* *OPTIONAL* flags:
    * ```[-k]``` k value to use; defaults to 3.
    * ```[-d]``` distance function to use, one of: euclidean .squared "e2" (default) or manhattan "manh".
    * ```[-unitw]``` whether to use unit voting weights; defaults to 1/d weights.
    * [--help] for help.
* *REQUIRED* flags:
    * ```[-train]``` a file containing training data.
    * ```[-test]``` a file containing points to test.
  
----

To compile and run *K-Means*:
```bash
python path [-d $distance] -data $train [centroid_1,centorid_2,...]
```
Example:
```bash
python3 ./kmeans.py -d e2 -data some-input.txt 0,500 200,200 1000,1000
python3 ./kmeans.py -d manh -data some-input.txt 0,500,0 200,200,200 1000,1000,1000

```

Where:
* *OPTIONAL* flags:
    * ```[-d]``` distance function to use, one of: euclidean .squared "e2" (default) or manhattan "manh".
    * [--help] for help.
* *REQUIRED* flags:
    * ```[-data]``` a file containing points to cluster.
* *REQUIRED* inputs:
    * ```[list of centroids]``` a space separated, comma separated representation of centroid coordinates/values

## Implementation Details
The implementation follows the specifications as provided by Professor Paul Bethe from NYU in the course of CSCI-GA.2560 Artificial Intelligence and is completely built by scratch with python native data types and built-in libraries:

### kNN Algorithm
- The training file will be a csv consisting of lines with the same N+1 columns. Where the first N columns are predictive attributes which will be integers, and the last entry can be any alphanumeric identifier. Blank lines should be ignored. There will be no "null" attributes to worry about.

- The test file is identical to the training file, but you will use the classification attribute for measuring accuracy.

- Algorithm: predict classification of each entry in the test file by running kNN against the training file. Then use the provided label in the test file to record correctness.
#### kNN Output
 - The program should output the target/wanted label and the actual label in the order listed in the file.

- At the end of program run, Precision and Recall reported separately for each labe.

### kMeans Algorithm
- The training file will be a csv consisting of integer data points in any N dimensional plane

- Each line will contain N comma-separated integer points plus a final alphanumeric 'label' used for printing

- The points should all have the same N dimensions which also match the given centroids.

- The number of centroids "K" is inferred from the command-line input of centroids.

- Run kMeans using the chosen distance function, alternating clustering and re-computing centroids until the centroids converge and do not change.

#### kMeans Output
- The program should output the final centroids using cluster-number aliases (C1, C2, C3, ...), and then print how the inputs were clustered by label.