"""
     get_lemmas.py

     This script uses the morphology tier to extract lemmas from a CHILDES
     Corpus. These lemmas can be used to create specific mean-length of
     utterance counts for individual words.

     Function: get_lemmas(filename, outname)- collects all unique lemmas from
                                              a CHILDES corpus

     Joseph Coffey
     Infant Language Acquisition Lab
     Professor: Dr. Dan Swingley
     Manager: Elizabeth Crutchley
     Last Updated: 12/14/16


"""

import sys, re

def get_lemmas(filename, outname):
    lms = []
    with open(outname, 'wb') as outf:
        with open(filename, 'r') as readf:
            data = readf.readlines()
            for l in data:
                if "%mor:" in l:
                    words = re.findall(r'(?<=\|)\w+', l)
                    for w in words:
                        if w not in lms:
                            lms.append(w)
        for lm in lms:
            outf.write(lm + '\n')

 
if __name__ == '__main__':
    get_lemmas(sys.argv[1], sys.argv[2])
