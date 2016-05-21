# Image search

### Installation
- To try it out, clone the repository. Make sure to have opencv 3.0.0 installed. 
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

