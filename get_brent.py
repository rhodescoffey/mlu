"""
    get_brent.py

    This program creates a .csv file containing the utterance, morphology,
    and grammatical relation tier of each utterance in the Brent corpus,
    organized by mother. Additionally, the file includes information about
    the length of utterance in words, morphemes, and relations.

    This file can then be used as an argument to get_mlu.py to get the mean
    length of utterance in these different metrics for each lemma, organized
    by mother.

    Functions: get_brent(filename)- Outputs .csv file of utterance length data.

    CHANGES TO CORPUS:
    ----Text Removed----
    In each tier, annotation irrelevant to the analysis was removed using
    regular expressions, listed below.
    *MOT: \[(.*?)\]|\((.*?)\)|\@\w+|\&\=\w+|\&\w+|www|xxx|[_+:]|\*MOT:|\d+|\*EVA:
          \[(.*?)\] -- Removes bracketed content
          \((.*?)\) -- Removes parethetical content
          \@\=\w+ -- Removes content preceded by "@="
          \&\=\w+ -- Removes content preceded by "&="
          \&\w+ -- Removes content preceded by "&"
          www -- Removes non-infant directed speech
          xxx -- Removes unintelligible speech
          \*MOT: -- Removes tier label
          \d+ -- Removes numerical content
          \*EVA: -- Removes alternate tier label
          [_+:] -- Removes punctuation for compounds

    %mor: %mor:\t|cm\|cm|bq\|bq|eq\|eq|(?<=\w)\+\w+\||[!.?_]
          %mor:\t -- Removes tier label
          cm\|cm -- Removes comma annotation
          bq\|bq -- Removes quotations
          eq\|eq -- Removes quotations
          (?=\w)\+\w+\| -- Removes compound marking, allows for extraction
                              of compound as lemma
          [!.?_] -- Removes punctuation

    %gra: \d+\|\d+\|PUNCT -- Removes punctuation label


    ----CDI Analysis----
    In processing the raw Brent corpus, several changes were made to the corpus
    data to allow CDI data to be extracted.
        - Some lemmas in the CDI were counted as two separate nouns in the 
          Brent Corpus. These nouns were changed to single words but counted
          as two morphemes (i.e. compound nouns).
        - Some lemmas were changed to their corresponding plural form for the
          purpose of headers. These lemmas included all instances of both
          plural and singular form, except for GLASSES, which was counted as
          its own lemma, rather than as GLASS-PL.
        - Similarly, YUCKY and SCARED are listed as lemmas, and include all
          instances of YUCK and SCARE. These changes, as well as the plural
          changes, are documented in get_mlu.py.
        - TEACHER and POTTY are counted as their own lemmas, and do not include
          instances of TEACH or POT. Likewise is ZIPPER separated from ZIP.
          WANNA, on the other hand, is still counted as two morphemes.
        - CDI changes involving a change in morphemes occur BEFORE counting,
          and changes involving no change in morphemes but a change in word
          count occur AFTER counting. Listings can be found in
          CDI_BEFORE_MORPHS and CDI_AFTER_MORPHS.
        - As of now, the %GRA tier is unchanged.
        - Note for future analyses: count all derived forms as distinct lemmas.

    Joseph Coffey
    Infant Language Acquisition Lab
    Professor: Dr. Dan Swingley
    Manager: Elizabeth Crutchley.
    Last Updated: 7/11/16

"""

import re, sys, csv


CDI_WORDS = {"all gone":"allgone", "bath tub":"bathtub", 
             "fire truck":"firetruck", "ice cream":"icecream", "t_v":"tv"}

CDI_BEFORE_MORPHS = {"n|glass-PL":"n|glasses", "n|pot-DIM":"n|potty",
                     "n|t_v":"n|tv", "n|teach&dv-AGT":"n|teacher",
                     "bi#n|cycle":"n|bicycle", "adj|sleep&dn-Y":"adj|sleepy",
                     "n|zip&dv-AGT":"n|zipper", "adj|dirt&dn-Y":"adj|dirty", 
                     "n|child&PL":"n|children", 
                     "part|break&PASTP":"part|broken",
                     "adj|care&dn-FULL":"adj|careful", "n|foot&PL":"n|feet", 
                     "n|person&PL":"n|people", "adj|pen&dn-Y":"n|penny", 
                     "n|stroll&dv-AGT":"n|stroller", 
                     "v|tire-PAST":"part|tired", 
                     "part|tire-PASTP":"part|tired",
                     "v|fall&PAST":"v|fell"}

CDI_AFTER_MORPHS = {"adv|all part|go&PASTP":"co|allgone", 
                    "n|bath n|tub":"n|bathtub", "n|fire n|truck":"n|firetruck",
                    "n|ice n|cream":"n|icecream", "v|want~inf|to":"v|wanna"}


def get_brent(filename):
    out = "brent_data_cdi.csv"
    utter = ''  # Content of mother tier
    morph = ''  # Content of mor tier
    gram = ''  # Content of gra tier
    sect = ''  # Which section are we at?
    lu = 0  # Length of utterance in words
    lum = 0  # Length of utterance in morphemes
    lug = 0  # Length of utterance in grammatical relations
    mom = ''  # Which mom is it?
    child = False  # Do nothing when child is speaking
    mothers = ("*MOT:", "*EVA:", "*OTH:")


    """ For checking if removing affected speech affects MLU """
    affect = ("[=! voice]", "[=! read]", "[=! sung]", "[=! whispered]")
    affected = False  # Do nothing when speech is affected
    out = "brent_affect_data.csv"

    """ Initialize data file """
    with open(out, 'wb') as outf:
        data_writer = csv.writer(outf)
        data_writer.writerow(["mom","age","utter","mrph","grm","lu","lum","lug"])

        """ Determine if lines are sung, read, or otherwise affected """
        with open(filename, 'r') as readf:
            data = readf.readlines()
            for l in data:
                for a in affect:
                    if a in l:
                        continue  # Skip 

                if "---" in l:
                    mom = re.findall(r'\w\d(?=\-)', l)[0]
                    age = re.findall(r'(?<=\-)\d{2}', l)[0]

                """ Start looking for new MOT/named mother """
                for m in mothers:
                    if m in l:
                        if gram != '':
                            e = [mom,age,utter,morph,gram,str(lu),str(lum),str(lug)]
                            data_writer.writerow(e)
                            morph = ''
                            gram = ''
                            lum = 0
                            lug = 0
                        sect = 'mot'
                        utter = ''
                        lu = 0
                        child = False
                        affected = False

                """ Do nothing if child is speaking """
                if "*CHI" in l or "*MAG" in l:
                    child = True

                """ Raise boolean flag if line is sung, read, or affected """
                for a in affect:
                    if a in l:
                        affected = True

                """ Start looking for new mor """
                if "%mor" in l and not child and not affected:
                    sect = 'mor'

                """ Start looking for new gra """
                if "%gra:" in l and not child and not affected:
                    sect = 'gra'

                """ If still looking for MOT """
                if sect == 'mot':
                    for i in CDI_WORDS:
                        if i in l:
                            l = l.replace(i, CDI_WORDS[i])
 
                    """ Remove brackets, parens, noise, MOT, #'s, conjuncts """
                    sb = r'\[(.*?)\]|\((.*?)\)|\@\w+|\&\=\w+|\&\w+|www|xxx|[_+:]|\*MOT:|\d+|\*EVA:|\*OTH:'
                    words = re.findall(r'[a-zA-Z\']+', re.sub(sb, '', l))
                    format_l = ''
                    for w in words:
                        lu += 1
                        format_l += (w + ' ')
                    utter += format_l


                """ If still looking for mor """
                if sect == 'mor':
                    for i in CDI_BEFORE_MORPHS:
                        if i in l:
                            l = l.replace(i, CDI_BEFORE_MORPHS[i])

                    """ Remove annotated non-morphemes and compounds """
                    not_mor = r'%mor:\t|cm\|cm|bq\|bq|eq\|eq|(?<=\w)\+\w+\||[!.?_]'
                    """ Removes punctuation """
                    mors = re.sub(not_mor, '', l)
                    format_l = ''
                    for ch in mors:
                        format_l += ch
                        """ Counts number of morphemes by '|' or '-' """
                        if ch == '|' or ch == '-':
                            lum += 1

                    """ Apply CDI morph conversion AFTER morphs are counted """
                    for i in CDI_AFTER_MORPHS:
                        if i in format_l:
                            format_l = format_l.replace(i, CDI_AFTER_MORPHS[i])
                    morph += format_l


                """ If still looking for gra """
                if sect == 'gra':
                    """ Find number of grammatical relationships """
                    gramms = r'\d+\|\d+\|\w+'
                    """ Removes punctuation """
                    not_gramms = r'\d+\|\d+\|PUNCT'

                    """ Remove non-grammatical relations to find real ones """
                    grs = re.findall(gramms, re.sub(not_gramms, '', l))
                    format_l = ''
                    for g in grs:
                        lug += 1
                        format_l += (g + ' ')
                    gram += format_l


if __name__ == '__main__':
    get_brent(str(sys.argv[1]))
