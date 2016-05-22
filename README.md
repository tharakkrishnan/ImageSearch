# Image search

### Installation
- To try it out, clone the repository. Make sure to have opencv 3.0.0 installed.You would also need opencv_contrib installed. It contains the patented SIFT and SURF algorithms that are used for feature matching. 
- cd src
- ./run.sh

### Problem statement
The directory ImageSearch/modified_images contain images that are modified in various ways. The original images are on an account in Flickr. The modified images are scaled, rotated, contrast-changed versions of those on Flickr. The software will try to get the best match for the modified images.

### Overview of the solution
- In order to compare and obtain a match between images that is scaling, rotation, illumination and viewpoint, we need to extract features that are invariant to these modifications. SIFT (scale invariant feature transform) is a good fit for our needs. 
- We first apply SIFT on our universe space (all possible images that might contain the modified image) and obtain keypoints and descriptors.
- Then we apply SIFT and obtain keypoints and descriptors for each modified image.
- We then compare the descriptors of the modified image using a nearest neighbor match to and score it against all the descriptors in the universe
- The image in the universe with the highest score is the best match for the modified image.

### Implementation
- ingest.py fetches all the images in the universe to a folder under /tmp/ingest
- Next we extract scores(keypoints, descriptors) using SIFT for all files in /tmp/ingest using get_scores()
- Similarly we extract scores for the modified images under ../modified\_images using get\_scores()
- In a nested loop we iterate through the scores for each modified image comparing with those of an image from the universe using score\_match() which returns the number of good matches. 
- By keeping track of the maximum score we can obtain the best match in the universe for the modified image.

### Results
#### Initial run with SIFT and Brute force with K-nearest neighbor (set to 2 neighbors) gave us a recognition accuracy of 88%


### Future implementations for robustness and speed
- The current implementation can be easily optimized for speed by parallelizing a number of operations.
- ingest.py currently fetches a list of urls, and then downloads images from each url one by one. The downloads are I/O bound independent processes. It is possible to replicate ingest.py into 10 workers, each of which fetch, 1/10th of the urls and download images. The workers will also calculate the scores and place them in a distributed NoSQL data base or even amazon SQS for fast retreival. The images can be discarded after the scores are calculated to reduce memory overhead for large universes.
- process.py which obtains the match by comparing the modified image score with the scores of the universe can also be optimzed using a number of workers that split up the universe space and consolidate results at the end. This map-reduce process can potentially be implemented on a hadoop cluster.
- The computation of descriptors and the match process are the two compute heavy modules. Refactoring them and using an optimized C implementation may improve performance. 
- Further we can use a clustering algorithm (K means) to divide the universe into buckets with similar descriptors in order to improve the speed of the matching process. Start testing against the part of the universe with highest match. This maybe especially useful for video frames that may contain highly correlated data.
- There maybe better feature extraction and image matching algorithms like SURF or ORB which can be used. Perhaps they can all be used simultaneously to improve prediction accuracy. 
- Need to examine failed cases to figure out why they failed.


