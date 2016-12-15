"""
    cat_files.py

    This file concatenates the .cha files in the Brent corpus for analysis in
    a single, combined corpus. The files can be located in separate directories
    within the working directory of the program. Other .cha files will be added
    to corpus if found, so remove these from the directory before running this
    function.

    Function: cat_files()- combines .cha files of CHILDES corpora

    Joseph Coffey
    Infant Language Acquisition Lab
    Professor: Dr. Dan Swingley
    Manager: Elizabeth Crutchley
    Last Updated: 12/14/16

"""

import os, glob


def cat_files():
    direc = raw_input("Enter name for combined corpus: ")

    """ Create file for combined corpora """
    with open(direc, 'wb') as outf:

        """ Walk through directories with .cha files """
        for root, dirs, files in os.walk("."):
            for name in files:      
                if name.endswith(".cha"):
                    filepath = os.path.join(root, name)

                    """ Write to file """
                    with open(filepath, 'r') as readf:
                        f = readf.read()
                        outf.write("---" + name + "\n")
                        for l in f:
                            outf.write(l)
                        outf.write("\n\n")


if __name__ == '__main__':
    cat_files()
