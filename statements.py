# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen


# PART A: Processing statements

def add(lst,item):
    if (item not in lst):
        lst.insert(len(lst),item)


class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
        self.words = []

    def add(self, stem, cat):
        self.words.append((stem, cat))

    def getAll(self, cat):
        # returns list comprehension filtering by category and using set() for uniqueness
        return [x[0] for x in set(self.words) if x[1] == cat]


class FactBase:
    def __init__(self):
        self.unaryFacts = []
        self.binaryFacts = []

    def addUnary(self, sym, pred):
        self.unaryFacts.append((sym, pred))

    def addBinary(self, sym, pred1, pred2):
        self.binaryFacts.append((sym, pred1, pred2))

    def queryUnary(self, sym, pred):
        return (sym, pred) in self.unaryFacts

    def queryBinary(self, sym, pred1, pred2):
        return (sym, pred1, pred2) in self.binaryFacts


import re
import nltk
from nltk.corpus import brown


def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""
    vowels = "aeiou"

    stem = ""

    # Checks words ending in "ies"
    if re.match(".*ies$", s):
        if len(s) == 4 and not s[0] in vowels:
            stem = s[:-1]
        else:
            stem = s[:-3] + 'y'
    # Checks words ending in "es"
    elif re.match(".*es$", s):
        if re.match(".*(o|x|ch|sh|ss|zz)es$", s):
            stem = s[:-2]
        elif re.match(".*[^(sxyz)]es$", s) and s[-4:-2] != 'sh' and s[-4:-2] != 'ch':
            stem = s[:-1]
        elif re.match(".*(s|z)es$", s) and s[-4:-1] != ("sse" and "zze"):
            stem = s[:-1]
    # Checks words ending in "s"
    elif re.match(".*s$", s):
        if s == "has":
            stem = "have"
        elif s[-2] == 'y' and s[-3] in vowels:
            stem = s[:-1]
        elif re.match(".*[^(sxyz)]s$", s) and s[-4:-2] != 'sh' and s[-4:-2] != 'ch':
            stem = s[:-1]
    # if it doesn't end in "s"
    else:
        return s

    # checks if stem is an infinitive verb and that s was a third person verb
    # using a set of the collection of tagged words to improve performance
    if not ((stem, "VB") in set(nltk.corpus.brown.tagged_words()) and (s, "VBZ") in set(nltk.corpus.brown.tagged_words())):
        stem = ""
    return stem


def add_proper_name(w,lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w,'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement(lx,wlist,fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name (wlist[0],lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a','an']):
                lx.add (wlist[3],'N')
                fb.addUnary ('N_'+wlist[3],wlist[0])
            else:
                lx.add (wlist[2],'A')
                fb.addUnary ('A_'+wlist[2],wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add (stem,'I')
                fb.addUnary ('I_'+stem,wlist[0])
            else:
                msg = add_proper_name (wlist[2],lx)
                if (msg == ''):
                    lx.add (stem,'T')
                    fb.addBinary ('T_'+stem,wlist[0],wlist[2])
    return msg

# End of PART A.
