import email
import pickle
import os
import re
import nltk
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import wordnet
from bs4 import BeautifulSoup
from urlparse import urlparse

import utils

def open_label_file(file_label=""):
    with open(file_label, 'rb') as f:
        corpus = f.readlines()
    return corpus


def get_content_from_msg(filename):
    if not os.path.exists(filename): # dest path doesnot exist
        print "ERROR: input file does not exist:", filename
        return
    fp = open(filename)
    msg = email.message_from_file(fp)
    payload = msg.get_payload()
    if type(payload) == type(list()) :
        payload = payload[0] # only use the first part of payload
    sub = msg.get('subject')
    sub = str(sub)
    if type(payload) != type(''):
        payload = str(payload)
    soup = BeautifulSoup(payload, "lxml")
    payload = soup.get_text()
    if payload: 
        payload = payload.encode('utf-8')
        payload = payload.replace('\n', ' ').replace('\r', '').replace(',', '')
        a = ' '.join(payload)
    return payload


def process_href(link):
    parsed_uri = urlparse(link)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain

def process_word(word):
    if '://' in word:
        word_edit = process_href(word)
    word_edit = re.sub('[^A-Za-z0-9]+', '', word)
    word_edit = st.stem(word_edit.lower())
    return word_edit


def main(file_label="data/SPAMTrain.label"):
    corpus = open_label_file(file_label)
    st = LancasterStemmer()
    dataset = dict()
    dictionary_s = dict()
    dict_s_word_appearence = dict()
    dictionary_h = dict()
    dict_h_word_appearence = dict()
    S = list()
    H = list()
    S_len = 0
    H_len = 0
    for ex in corpus:
        ex_col = ex.split(' ')
        target = int(ex_col[0])
        msg_file = ex_col[-1].replace('\n','')
        msg_content = get_content_from_msg("data/train/" + msg_file)
        if not msg_content:
            continue
        msg_list = msg_content.split(" ")
        msg_indices = list()
        if target:
            d = dictionary_h
            d_appreance = dict_h_word_appearence
        else:
            d = dictionary_s
            d_appreance = dict_s_word_appearence
        for word in msg_list:
            word_edit = process_word(word)
            if word_edit not in d:
                end = len(d)
                d[word_edit] = end
                d_appreance[word_edit] = 1
                msg_indices.append(end)
            else: 
                d_appreance[word_edit] += 1
                msg_indices.append(d[word_edit])
        if target:
            H_len += len(msg_indices)
            H.append(msg_indices)
        else: 
            S_len += len(msg_indices)
            S.append(msg_indices)
    dataset['spam_word_indices'] = dictionary_s
    dataset['spam_word_appreance'] = dict_s_word_appearence
    dataset['spam_indices'] = S
    dataset['spam_total_example_length'] = S_len
    dataset['ham_word_indices'] = dictionary_h
    dataset['ham_word_appreance'] = dict_h_word_appearence
    dataset['ham_indices'] = H
    dataset['ham_total_example_length'] = H_len
    utils.save_file("data/dataset.txt", dataset)