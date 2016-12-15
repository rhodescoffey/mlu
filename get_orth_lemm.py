"""
    get_orth_lemma.py

    This program searches the .csv file created by get_brent.py and extracts
    information about each word, including its lemma and part of speech. The
    format of the orth_lemma .csv is as follows.

        mom    age    utter    lemma    pos
e.g.    c1     9(mos) liked    like     v

    Functions: get_orth_lemm(filein)- Outputs .csv file of lemma data from 
                                      corpus

    Joseph Coffey
    Infant Language Acquisition Lab
    Professor: Dr. Dan Swingley
    Manager: Elizabeth Crutchley
    Last Updated: 12/15/16

"""


import csv, sys, re

def get_orth_lemm(filein):
    newfile = "brent_lemma_to_ortho.csv"

    with open(filein, 'rb') as csvf:
        with open(newfile, 'wb') as newf:
            csvr = csv.reader(csvf)
            csvw = csv.writer(newf)
            csvr.next()
            csvw.writerow(["mom", "age", "utter", "lemma", "pos"])
            morphs = re.compile('(?<=\|)\w+')
            pos = re.compile('[a-zA-Z0-9\:]+(?=\|)')
            for row in csvr:
                print row
                ortho = row[2].split()
                lemma = row[3].split()
                for o, l in zip(ortho, lemma):
                    p = re.findall(pos, l)
                    lem = ' '.join(re.findall(morphs, l))
                    if len(p) > 1:
                        csvw.writerow([row[0], row[1], o, lem, p[0]+'~'+p[1]])
                    else:
                        csvw.writerow([row[0], row[1], o, lem, p[0]])


if __name__ == '__main__':
    get_orth_lemm(sys.argv[1])
