#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
from collections import Counter
from textblob import TextBlob
def main(args):
    THEMAX = 1E99
    minage = 0
    maxage = THEMAX
    if( len(args) >2 ):
        maxage = int(args[-1])
        minage = int(args[-2])
        print('Limiting to ages %s through %s' % (minage, maxage))
        
    words = input('words to search: ')
    words = words.lower().split()
    nounphrases = []
    died = 0
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
                        #print('age'+row[3])
                        #if(row[3] == ''):
                        #    print('unspecified age')
                        #    print(row)
                        if minage == 0 and maxage == THEMAX:
                            #symptom = TextBlob(text).correct()
                            #print(symptom.noun_phrases)
                            with open('found/'+row[3]+'yr-'+row[0]+'-'+row[6], 'w') as outfile:
                                outfile.write(text)
                            nounphrases += text.split()
                            if row[9] == 'Y':
                                #print(row)
                                died += 1
                            
                        elif row[3] != '' and float(row[3]) >= minage and float(row[3]) <= maxage:
                            #symptom = TextBlob(text).correct()
                            #print(symptom.noun_phrases)
                            with open('found/'+row[3]+'yr-'+row[0]+'-'+row[6], 'w') as outfile:
                                outfile.write(text)
                            nounphrases += text.split()
                            if row[9] == 'Y':
                                #print(row)
                                died += 1 
                linecount += 1
                #if linecount > 1000: #quick run?
                #    break;
    print('Died:%s' % (died,))
    c = Counter(nounphrases)
    for item in c.most_common(200):
        print(item)
                
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
