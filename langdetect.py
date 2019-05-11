import nltk
import sys
import utils

STOPWORDS_DICT = dict()
for lang in nltk.corpus.stopwords.fileids():
    STOPWORDS_DICT[lang] =  set(nltk.corpus.stopwords.words(lang))

def get_language(text):
    words = set(nltk.wordpunct_tokenize(text.lower()))
    return max(((lang, len(words & stopwords)) for lang, stopwords in STOPWORDS_DICT.items()), key = lambda x: x[1])[0]


def find_refs_languages(db,maxpriority,outfile):
    refs = get_references(db,maxpriority)
    print('refs : '+str(len(refs)))
    res=list()
    for ref in refs :
        id = ref['id']
        language = get_language(ref['title'])
        res.append(id+";"+language)
    f = open(outfile,'w')
    for row in res:
        f.print(row)
    f.close()

find_refs_languages('urbmod',int(sys.argv[1]),sys.argv[2])
