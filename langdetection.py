import nltk
import sys
import utils
from langdetect import detect_langs

# ensure determinsitic results for langdetect
langdetect.DetectorFactory.seed = 0

STOPWORDS_DICT = dict()
for lang in nltk.corpus.stopwords.fileids():
    STOPWORDS_DICT[lang] =  set(nltk.corpus.stopwords.words(lang))

def get_language_nltk(text):
    words = set(nltk.wordpunct_tokenize(text.lower()))
    return max(((lang, len(words & stopwords)) for lang, stopwords in STOPWORDS_DICT.items()), key = lambda x: x[1])[0]

def get_language(text):
    return(detect_langs(text))



def find_refs_languages(db,maxpriority,outfile):
    refs = utils.get_references(db,maxpriority)
    print('refs : '+str(refs.count()))
    res=list()
    for ref in refs :
        id = ref['id']
        #language = get_language_nltk(ref['title'])
        lang_probas = get_language(ref['title'])
	res.append(id+";"+language)
    f = open(outfile,'w')
    for row in res:
        f.write(row+'\n')
    f.close()

#find_refs_languages('urbmod',int(sys.argv[1]),sys.argv[2])
find_refs_languages(sys.argv[1],int(sys.argv[2]),sys.argv[3])

