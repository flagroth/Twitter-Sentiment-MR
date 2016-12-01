#!/usr/bin/env python2
import sys

curr_zipcode = None
curr_count = 0


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

# Output the count for the last word
if curr_zipcode == zipcode:
    print '{0}\t{1}'.format(curr_zipcode, curr_count)
