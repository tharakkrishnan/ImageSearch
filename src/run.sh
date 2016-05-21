#/usr/bin/bash

which python

echo "Fetching the universe of pictures from flickr..." 
python ingest.py
echo "Extract features from modified images, followed by extract features from Universe, then for each modified image find a picture in the universe with the best match"
python process.py
echo "Computing accuracy of the results compared with known samples"
python score_test.py computed_results.csv
