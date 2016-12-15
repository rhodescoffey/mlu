"""
    get_mlu.py

    This script gets the mean length of utterance according to an input metric
    (either by words, morphemes, or grammatical dependencies) for each lemma
    occuring in the utterances of each mother in the Brent corpus. This
    includes both early and late data.

    The output .csv file is of the following format:
    mom   lemma   utterances (i.e. number of times it occurs)   mlu

    For lemmas with an utterance count of zero, the mlu is the mlu averaged
    across the remaining mothers.

    Functions: get_mlu(csvvile, data='mlum')- gets the mean length of utterance
               according to a specified metric [data], set to morphemes by
               default, from a .csv file produced by get_brent.py. Calls
               functions from gld.py to get a dictionary and list of lemmas
               for processing. Acceptable values for data are 'mlu', 'mlum',
               and 'mlug' (no input --> 'mlum'; different input --> 'mlug').

    Joseph Coffey
    Infant Language Acquisition Lab
    Professor: Dr. Dan Swingley
    Manager: Elizabeth Crutchley
    Last Updated: 6/30/16

"""


import csv, re, sys, gld


CDI_REPLACE = {"bead":"beads", "bubble":"bubbles", "carrot":"carrots",
               "key":"keys", "noodle":"noodles", "scare":"scared", 
               "stair":"stairs", "thirst":"thirsty", "yuck":"yucky",
               "pea":"peas"}


def get_mlu(csvfile, data='mlum'):
    """ Get dict of lemmas organized by mom and output list of lemmas """
    m, word_list = gld.gld(csvfile)
    mlu_header = ''

    """ For setting row for data extraction, e.g. row[4] for mlu """
    if data == 'mlu':
        i = 5
        mlu_header = 'mlu'

    elif data == 'mlum':
        i = 6
        mlu_header = 'mlum'

    else:
        i = 7
        mlu_header = 'mlug'

    """ File to be created """
    newfile = "brent_" + data + ".csv"

    with open(newfile, 'wb') as readf:
        mlumwriter = csv.writer(readf)

        """ File header """
        mlumwriter.writerow(['mom', 'word', 'totalal', 'totale', mlu_header, 
                             "instances", "isolal", "isole"])

        with open(csvfile, 'rb') as csvf:
            data_reader = csv.reader(csvf)

            """ Read rows in csv, find words corresponding to dict keys """
            for row in data_reader:
                wds = r'(?<=\|)[a-zA-Z]+|(?<=\_)[a-zA-Z]+'
                words = re.findall(wds, row[3])
                """ For each word key, append the LUM of the utterance """
                for w in words:
                    m[row[0]][w.lower()][0].append(float(row[i])) 
                    
                    """ If utterance is in early corpora (age < 12mos) """
                    if int(row[1]) < 12:
                        m[row[0]][w.lower()][1].append(float(row[i]))

        """ Get median of all mothers as default median """
        alt = gld.get_mommed(word_list, m)

        """ Make changes to lemma entry for CDI compliance """
        for i, j in CDI_REPLACE.iteritems():
            if j in alt:
                alt[j] += alt.pop(i)
            else:
                alt[j] = alt.pop(i)

            for mom in m:
                if j in m:
                    m[mom][j] += m[mom].pop(i)
                else:
                    m[mom][j] = m[mom].pop(i)

        """ Write mother, key, and data to new csv file """
        for key, val in m.items():
            for vk, vv in val.items():
                """ If no occurence of token for mother, use default median """
                if len(vv[0]) == 0:
                    mlumwriter.writerow([key, vk, len(vv[0]), len(vv[1]), 
                                         alt[vk], "NA", 0, 0])

                else:
                    gldm = gld.median(vv[0])
                    isolal = 0
                    """ Get # of occurrences in isolation for all corpora """
                    for al in vv[0]:
                        if al == 1:
                            isolal += 1

                    isole = 0
                    """ Get # of occurrences in isolation for early corpora """
                    for e in vv[1]:
                        if e == 1:
                            isole += 1
                    mlumwriter.writerow([key, vk, len(vv[0]), len(vv[1]), 
                                         gldm, gldm, isolal, isole])


if __name__ == '__main__':
    get_mlu(str(sys.argv[1]), str(sys.argv[2]))
