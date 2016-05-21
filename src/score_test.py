import simplejson as json
import sys
import csv

def load_csv(csv_name):
    output_dict = {}
    with open(csv_name) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            output_dict[row[0]] = row[1]
    return output_dict

def score(ground_truth, predictions):
    num_correct = 0
    error_cnt=0
    num_matched = len(ground_truth.keys())
    for filename in ground_truth.keys():
        try:
            if ground_truth[filename].strip() == predictions[filename].strip():
                num_correct+=1
        except Exception as e:
		error_cnt += 1
		print "{}/{}. Error: {} {}".format(error_cnt, num_matched, type(e).__name__, e.args)
            	pass
    print "num_correct:{}".format(num_correct) 	
    accuracy  = float(num_correct)/float(num_matched)
    return accuracy

if __name__ == "__main__":
    #make sure the script is being used correctly
    if len(sys.argv) != 2:
        print("Incorrect usage! Correct usage is:\npython score_results.py <your csv file>")
        sys.exit()

    #make sure file is a .csv
    filename = str(sys.argv[1])
    if not filename.endswith(".csv"):
        print("must be csv file ending with '.csv' !")
        sys.exit()

    #load the validation set data
    val_gt = load_csv('validation_set.csv')

    #go through the csv and score the results
    val_preds = load_csv(filename)

    #get results
    results = score(val_gt, val_preds)
    print("Accuracy: {}".format(results))

    
            

