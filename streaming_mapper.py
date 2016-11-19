#!/usr/bin/env python2

import sys
import json
import unicodedata
import re, string
import csv


def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()
    
def solo_letras ( text ):
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('',text)

reload(sys)
sys.setdefaultencoding('utf8')

sentimientos = {}
palabras = csv.DictReader(open('Redondo_words_comas.csv'),fieldnames=['key','value'])
for p in palabras:
    p['key'] = elimina_tildes(p['key'])
    sentimientos[p['key']] = p['value']

# Read each line from STDIN
for line in sys.stdin:
    try:
        record = json.loads(line,encoding='latin-1')
    except ValueError:
        pass
    if record["lang"]=="es":
        # Get the words in each line
        line = record["text"]
        line = line.encode('utf8')
        words = line.split()

        # Generate the count for each word
        for word in words:  
            word = elimina_tildes(word)  
            word = solo_letras(word)
            if sentimientos.has_key(word):
            # Write the key-value pair to STDOUT to be processed by the reducer.
            # The key is anything before the first tab character and the value is
            # anything after the first tab character.
                print '{0}\t{1}'.format(word, sentimientos[word])
