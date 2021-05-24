#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
from collections import Counter
from textblob import TextBlob
def main(args):
    words = input('words to search: ')
    words = words.lower().split()
    nounphrases = []
    #log:
    if not os.path.isdir('found'):
        os.mkdir('found')
    for csvfile in ['2020VAERSData.csv', '2021VAERSData.csv']:
        #(Find the encoding when opening with a text editor like Geany)
        with open(csvfile,encoding='ISO-8859-1') as infile:
            linecount = 0
            for row in csv.reader(infile, delimiter=','):
                if linecount == 0:
                    print (f'Column names are {", ".join(row)}')
                else:
                    text = row[8]
                    found = True
                    for w in words:
                        if text.lower().find(w)==-1:
                            found = False; # Not found skip this record
                    if found:
                        symptom = TextBlob(text).correct()
                        print(symptom.noun_phrases)
                        with open('found/'+row[3]+'yr-'+row[0]+'-'+row[6], 'w') as outfile:
                            outfile.write(text)
                        nounphrases += symptom.noun_phrases
                linecount += 1
                #if linecount > 1000: #quick run?
                #    break;
    c = Counter(nounphrases)
    for item in c.most_common(200):
        print(item)
                
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
