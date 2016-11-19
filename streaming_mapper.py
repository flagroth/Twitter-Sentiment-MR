#!/usr/bin/env python2

import sys
import json

# Read each line from STDIN
for line in sys.stdin:
   record = json.loads(line,encoding='latin-1')
   # Get the words in each line
   line = record["text"]
   line = line.encode('utf8')
   words = line.split()

   # Generate the count for each word
   for word in words:

      # Write the key-value pair to STDOUT to be processed by the reducer.
      # The key is anything before the first tab character and the value is
      # anything after the first tab character.
      print '{0}\t{1}'.format(word, 1)
