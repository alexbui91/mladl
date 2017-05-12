import utils
import process_data as p
import numpy as np


dataset = None


def main():
    global dataset
    dataset = utils.load_file('data/dataset.txt')
    spam_docs_len = len(dataset['spam_indices'])
    ham_docs_len = len(dataset['ham_indices'])
    total = spam_docs_len + ham_docs_len
    spam_prob = get_prob(spam_docs_len, total)
    ham_prob = get_prob(ham_docs_len, total)


def get_prob(x, total):
    return x * 1.0 / total


def get_message_prob(msg_content):
    msg_list = msg_content.split(" ")
    s_msg_prob = h_msg_prob = 1.
    for word in msg_list:
        word_edit = p.process_word(word)
        prob_s, prob_h = get_word_prob(word_edit)
        s_msg_prob *= prob_s
        h_msg_prob *= prob_h
    l_radio = log_ratio_prob(h_msg_prob, s_msg_prob)
    return l_radio > 0


def get_word_prob(word):
    s_set = dataset['spam_word_appreance']
    h_set = dataset['ham_word_appreance']
    s_words_len = dataset['spam_total_example_length']
    h_words_len = dataset['ham_total_example_length']
    #default 
    s_prob = h_prob = 0.5
    if word in s_set:
        s_appearance = s_set[word]
        s_prob = get_prob(s_appearance, s_words_len)
    if word in h_set:
        h_appearance = h_set[word]
        h_prob = get_prob(h_appearance, h_words_len)
    return s_prob, h_prob


def log_ratio_prob(prob_h, prob_s):
    if not prob_s:
        prob_s = 1.0
    return np.log(prob_h/prob_s)