__author__ = 'Damcy'
# Copyright (c) 2014年 Damcy. All rights reserved.
# e-mail: stmayue@gmail.com
# Filename: assignment3.py

import re
import pickle
import os
import codecs
import math
from collections import Counter


def find_max_ele(my_dict):
    max_pos = None
    max_value = float("-inf")
    for item in my_dict:
        if my_dict[item] > max_value:
            max_pos = item
            max_value = my_dict[item]

    return max_pos


def smooth(w_i_1, t_j, tags, word_count, tag_count, a_count, b_count):
    if word_count[w_i_1] == 0:
        # 连续两个词没有出现？how to do?
        # log1为 0
        return 1

    temp = 0
    for item in tags:
        times = b_count[(item, w_i_1)] * a_count[(item, t_j)] / word_count[w_i_1] / tag_count[item]
        temp += times

    return temp/tag_count[t_j]


def use_log(to_change):
    for item_1 in to_change:
        for item_2 in to_change[item_1]:
            if to_change[item_1][item_2] < 0.0000000000000000000001:
                print(item_1, item_2)

                print(to_change[item_1])
                print(to_change[item_1][item_2])
            to_change[item_1][item_2] = math.log(to_change[item_1][item_2])

    return to_change


def viterbi_tag(line, a, b, words, tags, word_count, tag_count, a_count, b_count):
    result_list = list()
    line_word = re.findall('\S+', line)
    if len(line_word) == 0:
        return ""

    # init delta and psi
    delta = dict()
    psi = dict()
    for i in range(0, len(line_word)):
        delta[i] = dict()
        psi[i] = dict()
    for i in range(0, len(line_word)):
        for item in tags:
            delta[i][item] = float("-inf")
            psi[i][item] = 0
    delta[0]['/m'] = 0
    # viterbi
    for i in range(1, len(line_word)):
        for item_1 in tags:
            for item_2 in tags:
                if line_word[i] in words:
                    if not a[item_2].get(item_1, 0) or not b[item_1].get(line_word[i], 0):
                        temp = float("-inf")
                    else:
                        temp = delta[i-1][item_2] + a[item_2].get(item_1, 0) + b[item_1].get(line_word[i], 0)
                else:
                    temp_b = smooth(line_word[i-1], item_1, tags, word_count, tag_count, a_count, b_count)
                    if not temp_b or not a[item_2].get(item_1, 0):
                        temp = float("-inf")
                    else:
                        temp = delta[i-1][item_2] + a[item_2].get(item_1, 0) + math.log(temp_b)
                if temp > delta[i][item_1]:
                    delta[i][item_1] = temp
                    psi[i][item_1] = item_2
    # track back
    position = find_max_ele(delta[len(line_word) - 1])
    temp_list = list()
    for i in range(len(line_word)-1, -1, -1):
        temp_list.append(position)
        position = psi[i][position]
    # merge
    temp_list.reverse()
    for i in range(0, len(line_word)):
        result_list.append(line_word[i] + temp_list[i])

    return "  ".join(result_list)


def roll_back(result_line, num_mark, ch_num_mark, line_mark):
    for item in num_mark:
        if item[0] != "":
            result_line = re.sub('<n>', item[0], result_line, 1)
        else:
            result_line = re.sub('<n>', item[2], result_line, 1)

    for item in ch_num_mark:
        result_line = re.sub('<N>', item, result_line, 1)

    for item in line_mark:
        result_line = re.sub('<m>', item, result_line, 1)

    return result_line


def pre_process(line):
    pre_num = re.compile('([０-９]+(·|．|／)[０-９]+)|([０-９]+)')
    pre_ch_num = re.compile('[○零一二三四五六七八九十百千万亿]+')
    pre_line_mark = re.compile('[0-9]*-[0-9]*-[0-9]*-[0-9]*')
    line = pre_num.subn("<n>", line)[0]
    line = pre_ch_num.subn("<N>", line)[0]
    line = pre_line_mark.subn("<m>", line)[0]
    return line


def find_num(line):
    pre_num = re.compile('([０-９]+(·|．|／)[０-９]+)|([０-９]+)')
    return pre_num.findall(line)


def find_ch_num(line):
    pre_ch_num = re.compile('[○零一二三四五六七八九十百千万亿]+')
    return pre_ch_num.findall(line)


def find_line_mark(line):
    pre_line_mark = re.compile('[0-9]*-[0-9]*-[0-9]*-[0-9]*')
    return pre_line_mark.findall(line)


def tagging(a, b, words, tags, word_count, tag_count, a_count, b_count):
    input_pointer = codecs.open("corpus_for_ass3test.txt", "r", "GBK")
    output_pointer = codecs.open("2011211672.txt", "w", "GBK")

    a = use_log(a)
    b = use_log(b)

    for (num, line) in enumerate(input_pointer):
        if len(line) == 0:
            output_pointer.write(os.linesep)
        else:
            num_mark = find_num(line)
            ch_num_mark = find_ch_num(line)
            line_mark = find_line_mark(line)
            line = pre_process(line)

            result_line = viterbi_tag(line, a, b, words, tags, word_count, tag_count, a_count, b_count)
            result = roll_back(result_line, num_mark, ch_num_mark, line_mark)
            output_pointer.write(result + os.linesep)

    output_pointer.close()
    input_pointer.close()


def load_a():
    # 词 转换为 tag 的概率
    fq = open("a_dict.data", "rb")
    a_dict = pickle.load(fq)
    fq.close()
    return a_dict


def load_b():
    # tag 之间转换概率
    fq = open("b_dict.data", "rb")
    b_dict = pickle.load(fq)
    fq.close()
    return b_dict


def load_word_list():
    # training set 中的词表
    fq = open("word_list.data", "rb")
    word_list = pickle.load(fq)
    fq.close()
    return word_list


def load_tag_list():
    # 训练样例中存在的tag集
    fq = open("tag_list.data", "rb")
    tag_list = pickle.load(fq)
    fq.close()
    return tag_list


def load_word_count():
    #训练样例中存在的word集
    wcq = open("word_count_data", "rb")
    word_count = pickle.load(wcq)
    wcq.close()
    return word_count


def load_tag_count():
    #tag 计数
    tcq = open("tag_count_data", "rb")
    tag_count = pickle.load(tcq)
    tcq.close()
    return tag_count


def load_a_pair():
    # 状态(tag)间转移计数
    acq = open("a_pair_data", "rb")
    a_count = pickle.load(acq)
    acq.close()
    return a_count


def load_b_pair():
    # 发射矩阵计数
    bcq = open("b_pair_data", "rb")
    b_count = pickle.load(bcq)
    bcq.close()
    return b_count


if __name__ == "__main__":
    a_dict = load_a()
    b_dict = load_b()
    word_list = load_word_list()
    tag_list = load_tag_list()
    # 处理未登录词要用到的数据
    word_count = load_word_count()
    tag_count = load_tag_count()
    a_count = load_a_pair()
    b_count = load_b_pair()
    #进行POS
    tagging(a_dict, b_dict, word_list, tag_list, word_count, tag_count, a_count, b_count)
