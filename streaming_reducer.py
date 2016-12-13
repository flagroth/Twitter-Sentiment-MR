#!/usr/bin/env python
import sys
import urllib
import csv
#import seaborn as sns
#import pandas as pd

curr_zipcode = None
curr_count = 0

opener = urllib.URLopener()
csvFile = opener.open('https://s3-eu-west-1.amazonaws.com/urjc.datascience.jcano/tweets/postal_codes.csv')
list_cps = csv.DictReader(csvFile,fieldnames=['key','value'])
cps = {}
# Process each key-value pair from the mapper
for line in sys.stdin:

    # Get the key and value from the current line
    try:
        zipcode, count = line.split('\t')
        zipcode = zipcode[:2]
    except ValueError:
        print 'ValueError'
        

    # Convert the count to an float
    count = float(count)

    if not(curr_zipcode):
        curr_zipcode = zipcode
    # If the current word is the same as the previous word, increment its
    # count, otherwise print the words count to STDOUT
    if zipcode == curr_zipcode:
        curr_count += count
    else:     
        # Write word and its number of occurrences as a key-value pair to STDOUT
        if curr_zipcode:
            print '{0}\t{1}'.format(curr_zipcode, curr_count)
            curr_zipcode = zipcode
            curr_count = count
    cps[curr_zipcode] = curr_count 
    
# Output the count for the last word
if curr_zipcode == zipcode:
    print '{0}\t{1}'.format(curr_zipcode, curr_count)


#sents=pd.DataFrame.from_dict(cps, orient="index")
#for x in cps:
#    print(x, float(cps[x]))

#sents.plot(kind='bar').get_figure().savefig("plot.png")
