import wikipedia
import re
import os
import codecs
import collections
import sys
import math
from itertools import islice, tee


method = input('which method? (w/ng)')
def intersection(a, b):
    out = []
    for i in a:
        if i in b:
            out.append(i)
    return out

def tokenize(text, method = method, ngrlen = 3):
    if method == 'w':
        return text.split(' ')
    else:
        N = ngrlen
        ngrams = zip(*(islice(seq, index, None) for index, seq in enumerate(tee(text, N))))
        ngrams = [''.join(x) for x in ngrams if len(intersection(x, [',', '.', '"', '-', '(', ')', ':', '?', '!', '—', ' ', '–', '«', '»', ';'])) == 0]
        return ngrams



def max_prob(probs):
    max = -1
    out = ''
    for i in probs:
        if probs[i] > max:
            out = i
    return out

def make_freq_list_text(text):
    freqs = collections.defaultdict(lambda: 0)
    for item in tokenize(text.replace('\n', '').lower(), method):
        freqs[item] += 1
    freqs = delete_from_dic(freqs,' :=-»«—!?().,')
    return freqs

def make_freq_list_corpus(corpus):
    freqs = collections.defaultdict(lambda: 0)
    merged_corpus = ' '.join(corpus)
    tokenized_corpus = tokenize(merged_corpus.replace('\n', '').lower(), method)
    corp_len = len(tokenized_corpus)
    for item in tokenized_corpus:
        freqs[item] += 1/corp_len
    freqs = delete_from_dic(freqs,' :=-»«—!?().,')
    return freqs


def delete_from_dic(dic, item_list):
    out = {}
    for i in dic:
        if i not in item_list:
           out[i] = dic[i]
    return out

def get_texts_for_lang(lang, n=10, test = 1):
    wikipedia.set_lang(lang)
    wiki_content = []
    pages = wikipedia.random(n)
    nprocessed = 0
    for page_name in pages:
        try:
            page = wikipedia.page(page_name)
            nprocessed += 1
            print (str(nprocessed/n))
        except wikipedia.exceptions.WikipediaException:
            print ('Skipping page {}'.format(page_name))
            continue
        wiki_content.append('{}\n{}'.format(page.title, page.content.replace('==', '')))
        try:
            if test == 1:
                fileout = open('test1/' + lang + '/' + str(page_name) + '.txt', 'w', encoding='utf-8')
            else:
                fileout = open(lang + '/' + str(page_name) + '.txt', 'w', encoding='utf-8')
        except:
            if test == 1:
                os.makedirs(('./test1/') + lang)
                fileout = open('test1/' + lang + '/' + str(page_name) + '.txt', 'w', encoding='utf-8')
            else:
                os.makedirs(('./') + lang)
                fileout = open(lang + '/' + str(page_name) + '.txt', 'w', encoding='utf-8')
            continue
        fileout.write(str('{}\n{}'.format(page.title, page.content.replace('==', ''))))
        fileout.close()
    return wiki_content

if input('get training texts? (y/n)') == 'y':
    for i in ['be','uk','kk','fr']:
       get_texts_for_lang(i, 100, 0)
if input('get test texts? (y/n)') == 'y':
    for i in ['be','uk','kk','fr']:
       get_texts_for_lang(i, 100, 1)

def get_freq_lists():
    wiki_texts = {}
    freq_lists = {}
    for i in ['kk', 'uk', 'be', 'fr']:
        wiki_texts[i] = []
        for root, dirs, files in os.walk('./' + i):
            for fnumber in range(0, len(files)):
                try:
                    curfile = open(i+'/' + files[fnumber], 'r', encoding='utf-8')
                    wiki_texts[i].append(curfile.read())
                    curfile.close()
                except:
                    continue
        freqs = make_freq_list_corpus(wiki_texts[i])
        freq_lists[i] = freqs
    return freq_lists

freq_lists = get_freq_lists()
#print(freq_lists['fr']['il'])

def define_lang_probability(text, lang):
    lang_freqs = freq_lists[lang]
    probab = 0
    for i in tokenize(text, method):
        if i in lang_freqs:
            probab += lang_freqs[i]*1000
    return probab

def define_text_language(text, langlist = ['be','fr','kk','uk']):
    text_freqs = make_freq_list_text(text)
    lang_probabs = {}
    for i in langlist:
        lang_probabs[i] = define_lang_probability(text, i)
    max = -1
    out = ''
    for i in lang_probabs:
        if lang_probabs[i] > max:
            out = i
            max = lang_probabs[i]
    return out

print (define_text_language('на вольны родны свой прастор.'))

for i in ['kk','uk','be','fr']:
    for root, dirs, files in os.walk('./test1/' + i):
        for fnumber in range(0, len(files)):
            try:
                curfile = open('test1/'+i+'/' + files[fnumber], 'r', encoding='utf-8')
                print(define_text_language(curfile.read(), ['kk','uk','be','fr']) +'  ' + files[fnumber])
                curfile.close()
            except:
                continue

