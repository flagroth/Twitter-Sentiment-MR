#!/usr/bin/env python2
import urllib
import urllib2
import sys
import json
import unicodedata
import re
import csv
#from geopy.geocoders import Nominatim
#from geopy.exc import GeocoderTimedOut

#gmaps = Nominatim(timeout=1)
opener = urllib.URLopener()
csvFile = opener.open('https://s3-eu-west-1.amazonaws.com/urjc.datascience.jcano/tweets/Redondo_words_comas.csv')

def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s.decode()
    
def solo_letras ( text ):
    regex = re.compile('[^a-zA-Z]')
    return regex.sub('',text)

reload(sys)
sys.setdefaultencoding('utf8')

sentimientos = {}
palabras = csv.DictReader(csvFile,fieldnames=['key','value'])
for p in palabras:
    p['key'] = elimina_tildes(p['key'])
    sentimientos[p['key']] = p['value']

# Read each line from STDIN
for line in sys.stdin:
    line = line.encode('utf8')
    try:
        record = json.loads(line,encoding='latin-1')
    except ValueError:
        pass
    if record["lang"]=="es":
        # Get the words in each line
        line = record["text"]
        coords = record["coordinates"]
        if coords is not None:
            lon = str(coords["coordinates"][0])
            lat = str(coords["coordinates"][1])
            #url = 'http://photon.komoot.de/reverse'
            url = 'http://54.154.150.47:2322/reverse'
            values = {'lon' : lon, 'lat' : lat}
            data = urllib.urlencode(values)
            full_url = url + '?' + data
            response = urllib2.urlopen(full_url)
            location_raw = response.read()
            location = json.loads(location_raw)
            #try:
            #    location = gmaps.reverse((lat, lon),timeout=1)
            #except GeocoderTimedOut as e:
            #    print "Error: geocode failed on input %s with message %s"%(location, e.msg)
            try:
                cp = location['features'][0]['properties']['postcode']
            except KeyError:
                continue

            words = line.split()

            valoracion = 0
            for word in words:  
                word = elimina_tildes(word)  
                word = solo_letras(word)
                if sentimientos.has_key(word):
                    valoracion = valoracion+float(sentimientos[word])
                # Write the key-value pair to STDOUT to be processed by the reducer.
                # The key is anything before the first tab character and the value is
                # anything after the first tab character.

            print '{0}\t{1}'.format(cp,valoracion)
                
