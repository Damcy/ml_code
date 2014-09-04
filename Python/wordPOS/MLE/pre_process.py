__author__ = 'Damcy'
# Copyright (c) 2014年 Damcy. All rights reserved.
# e-mail: stmayue@gmail.com
# Filename: pre_process.py

import re
import pickle
import os
import codecs
from collections import Counter
from itertools import islice


def saving_data(a_dict, b_dict, word_list, tag_list, word_count, tag_count, a_count, b_count):
    fq = open("a_dict.data", "wb")
    pickle.dump(a_dict, fq)
    fq.close()
    tq = open("b_dict.data", "wb")
    pickle.dump(b_dict, tq)
    tq.close()
    wq = open("word_list.data", "wb")
    pickle.dump(word_list, wq)
    wq.close()
    tq = open("tag_list.data", "wb")
    pickle.dump(tag_list, tq)
    tq.close()
    wcq = open("word_count_data", "wb")
    pickle.dump(word_count, wcq)
    wcq.close()
    tcq = open("tag_count_data", "wb")
    pickle.dump(tag_count, tcq)
    tcq.close()
    acq = open("a_pair_data","wb")
    pickle.dump(a_count, acq)
    acq.close()
    bcq = open("b_pair_data", "wb")
    pickle.dump(b_count, bcq)
    bcq.close()


def get_dict_sum(temp_dict):
    result = 0
    for item in temp_dict:
        result += temp_dict[item]

    return result


def normalization(temp_dict, total):
    for item in temp_dict:
        temp_dict[item] /= total

    return temp_dict


def data_process(a_count, b_count, word_list, tag_list, word_count, tag_count):
    a_dict = dict()
    b_dict = dict()
    for pair in a_count:
        if a_dict.get(pair[0], 0):
            a_dict[pair[0]][pair[1]] = a_count[pair]
        else:
            a_dict[pair[0]] = dict()
            a_dict[pair[0]][pair[1]] = a_count[pair]

    for pair in b_count:
        if b_dict.get(pair[0], 0):
            b_dict[pair[0]][pair[1]] = b_count[pair]
        else:
            b_dict[pair[0]] = dict()
            b_dict[pair[0]][pair[1]] = b_count[pair]

    for item in a_dict:
        total = get_dict_sum(a_dict[item])
        a_dict[item] = normalization(a_dict[item], total)

    for item in b_dict:
        total = get_dict_sum(b_dict[item])
        b_dict[item] = normalization(b_dict[item], total)

    saving_data(a_dict, b_dict, word_list, tag_list, word_count, tag_count, a_count, b_count)


def statistic():
    input_pointer = codecs.open("MLE_after.txt", "r", "GBK")

    a_count = Counter()
    b_count = Counter()
    word_count = Counter()
    tag_count= Counter()
    word_list = set()
    tag_list = set()

    for (num, line) in enumerate(input_pointer):
        words = re.findall("\S+", line)
        temp_tags = list()
        temp_words = list()
        for item in words:
            temp_words.append(re.sub('([^/]+)(/\S+)', '\\1', item))
            temp_tags.append(re.sub('([^/]+)(/\S+)', '\\2', item))

        for item in temp_words:
            word_list.add(item)
            word_count[item] += 1

        for item in temp_tags:
            tag_list.add(item)
            tag_count[item] += 1

        b_count += Counter(zip(temp_tags, temp_words))
        a_count += Counter(zip(temp_tags, islice(temp_tags, 1, None)))

    input_pointer.close()
    data_process(a_count, b_count, word_list, tag_list, word_count, tag_count)

if __name__ == "__main__":
    statistic()