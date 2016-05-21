#!/usr/bin/python
"""
        This module has methods that use the sift to calculate a score for a given image
"""
import cv2
import numpy as np
import os

DIR_TEST="../modified_images/"
DIR_UNIVERSE="/tmp/ingest"

global TRANSFORM
global MATCHER

def get_score(filename):
	try:
		img = cv2.imread(filename,0)
		kp, des = TRANSFORM.detectAndCompute(img, None)
		return (kp,des)
	except:
		print "ERROR: Unable to process file {} skipping...".format(filename)
		return (None, None)


def get_scores(files):
	scores_dict={}
	total = len(files)
	ctr = 0
	
	for f in files:
		ctr +=1
		print "Processing file {}/{}: {}".format(ctr, total, f)		
		_,fn = os.path.split(f)
		k,d = get_score(f)
		if k is not None and d is not None:
			scores_dict[fn] = (k,d)
	return scores_dict

def get_files_in_dir(directory):
	return [os.path.join(directory,f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


def match_scores(des1, des2):
	matches = MATCHER.knnMatch(des1,des2, k=2)
	# Apply ratio test
	good = []
	try:
		for m,n in matches:
    			if m.distance < 0.75*n.distance:
        			good.append([m])
		return len(good)
	except Exception as e:
		print "Error occured {}, {}".format(type(e).__name__, e.args)
		return 0



if __name__=="__main__":
	print cv2.__version__

	TRANSFORM = cv2.xfeatures2d.SIFT_create()
	MATCHER = cv2.BFMatcher()
	
	test_scores = {}
	test_scores = get_scores(get_files_in_dir(DIR_TEST))
	
	universe_scores = {}
	universe_scores = get_scores(get_files_in_dir(DIR_UNIVERSE))
	
	matched=[] 
	cnt = 0

	for test_k, test_v in test_scores.iteritems():
		match=(None, None, None)
		max_score = 0
		cnt += 1
		print "Matching {}/{}: {}".format(cnt, len(test_scores), test_k)
		for universe_k, universe_v in universe_scores.iteritems():
			score = match_scores(test_v[1], universe_v[1])
			if score > max_score:
				match = (test_k, universe_k, max_score)
				max_score = score
		
		matched.append(match)
	
	with open("computed_results.csv", "w") as f:
		for m in matched:
			line = "{},{}\n".format(m[0], m[1].replace("#","/").replace("farm8.","").replace("staticflickr","static.flickr").replace("https","http")) 
			f.write(line)
		
		
	
	
