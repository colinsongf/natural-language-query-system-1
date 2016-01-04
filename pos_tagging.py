# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'),
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]


def unchanging_plurals():
    singular_nouns = set()
    plural_nouns = set()
    unchanging = set()

    with open("sentences.txt", "r") as f:
        for line in f:
            for tagging in line.split():
                word, tag = tagging.split('|')
                if tag == 'NN':
                    singular_nouns.add(word)
                elif tag == 'NNS':
                    plural_nouns.add(word)

    for sn in singular_nouns:
        if sn in plural_nouns:
            unchanging.add(sn)

    return unchanging

unchanging_plurals_list = unchanging_plurals()


def noun_stem(s):
    """extracts the stem from a plural noun, or returns empty string"""
    vowels = "aeiou"

    stem = ""

    # Checks if word is an unchanging plurals
    if s in unchanging_plurals_list:
        return s
    # Checks if prefix is "men" (e.g. men, women)
    elif re.match(".*men$", s):
        stem = stem[:-3] + "man"
    # Else follow same rules as verb_stem (without corpus cross check)
    else:
        if re.match(".*ies$", s):
            if len(s) == 4 and not s[0] in vowels:
                stem = s[:-1]
            else:
                stem = s[:-3] + 'y'
        elif re.match(".*es$", s):
            if re.match(".*(o|x|ch|sh|ss|zz)es$", s):
                stem = s[:-2]
            elif re.match(".*[^(sxyz)]es$", s) and s[-4:-2] != 'sh' and s[-4:-2] != 'ch':
                stem = s[:-1]
            elif re.match(".*(s|z)es$", s) and s[-4:-1] != ("sse" and "zze"):
                stem = s[:-1]
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

    return stem


def tag_word(lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    tags = []

    # fetch the tag if the word is one of the given function words
    if wd in function_words:
        return [tag[1] for tag in function_words_tags if tag[0] == wd]

    # get proper noun and adjective matches from the lexicon
    tags += [tag for tag in ['P', 'A'] if wd in lx.getAll(tag)]

    # get verb (transitive and intransivite) matches from the lexicon, then tag singular or plural
    tags += [(tag + "p" if verb_stem(wd) == wd else tag + "s") for tag in ['I', 'T'] if verb_stem(wd) in lx.getAll(tag)]

    # get noun matches from lexicon, then tag singular or plural
    if noun_stem(wd) in lx.getAll('N'):
        if wd in unchanging_plurals_list:
            tags += ["Ns", "Np"]
        else:
            tags.append("Ns" if noun_stem(wd) == wd else "Np")

    return tags


def tag_words(lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]

# End of PART B.
