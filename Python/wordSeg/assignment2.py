__author__ = 'Damcy'
# Copyright (c) 2014年 Damcy. All rights reserved.
# e-mail: stmayue@gmail.com
# Filename: assignment2.py
# 利用 bi-gram 和 good turing 平滑实现的切分 demo

import codecs
import os
import re
import pickle
from itertools import islice
from collections import Counter


def calculate_final_p(count, total_pair, len_pair):
    '''
    计算 good turing

    先计算初始训练样本概率P，再根据平滑算法计算Pr，最后进行归一化
    通过 good turing 的计算方法来计算出现次数为 r 的平滑概率 turing_P[r]
    @param count: training set 统计的到的 bi-gram 计数
    @param total_pair: 整个 bi-gram 应该有的个数
    @param len_pair: 出现的 bi-gram 的个数
    @return:
    '''
    # Nr 为统计出现r次的 N-gram 出现的数目
    Nr = dict()
    # 已知词表中未曾出现(Nr[0])的 bi-gram 个数
    Nr[0] = total_pair - len_pair
    # 保存出现的pair数目：每一种pair的个数相加
    true_pair = 0

    max = 0
    for pair in count:
        true_pair += count[pair]
        if Nr.get(count[pair], 0):
            if count[pair] > max:
                max = count[pair]
            Nr[count[pair]] = Nr[count[pair]] + 1
        else:
            if count[pair] > max:
                max = count[pair]
            Nr[count[pair]] = 1
    print(max)
    # calculate P 初始概率，即出现次数大于1的bi-gram各自的概率
    P = dict()
    for i in range(0, max+1):
        if Nr.get(i, 0):
            P[i] = Nr[i] / true_pair
        else:
            P[i] = 0

    # calculate Pr
    Pr = dict()
    for i in range(0, max+1):
        if (Nr.get(i+1, 0) and Nr.get(i, 0)):
            Pr[i] = (i + 1) * Nr[i+1] / (Nr[i] * true_pair)
        else:
            Pr[i] = P[i]
    Pr_sum = sum(Pr.values())
    # 归一化
    turing_P = dict()
    for i in range(0, max+1):
        turing_P[i] = Pr[i] / Pr_sum
    # 返回平滑后的概率
    return turing_P


def good_turing(count, word_list):
    '''
    计算平滑概率，包括对所需数据的前期处理

    通过统计训练样本中的数据，得到需要的参数进行平滑计算，并将结果保存在文件中，并另存下一份可视化txt
    @param count: training set 中 bi-gram 计数
    @param word_list: training set 中出现的词语，作为词典使用
    @return: 平滑后的概率final_p
    '''
    # 词总个数
    len_list = len(word_list)
    # 完整的 bi-gram 表总共的个数
    total_pair = len_list * len_list
    # 训练样本中 bi-gram 的个数
    len_pair = len(count)

    # get turing_probability
    final_p = calculate_final_p(count, total_pair, len_pair)
    # save wat we get
    fq = open("turing.data", "wb")
    pickle.dump(final_p, fq)
    fq.close()
    tq = open("turing.txt", "w")
    for i in final_p:
        # print(i, final_p[i])
        tq.write(str(i) + " " + str(final_p[i]) + os.linesep)
    tq.close()

    return final_p


def saving_data(count, word_list):
    # save the result
    fq = open("count.data", "wb")
    pickle.dump(count, fq)
    fq.close()
    tq = open("word.data", "wb")
    pickle.dump(word_list, tq)
    tq.close()

    # save as readable txt
    # counter
    output_pointer_count = codecs.open("pair.txt", "w", "GBK")
    for pair in count:
        output_pointer_count.write(str(pair) + " " + str(count[pair]) + os.linesep)
    output_pointer_count.close()
    # word
    output_pointer_word = codecs.open("word.txt", "w", "GBK")
    for item in word_list:
        output_pointer_word.write(str(item) + os.linesep)
    output_pointer_word.close()


def pre_counting():
    '''
    对训练数据进行统计处理，得到bi-gram 和 词典
    '''
    input_pointer = codecs.open("corpus_for_ass2train.txt", 'r', "GBK")
    # init
    count = Counter()
    word_list = set()
    # 正则替换阿拉伯数字和中文句子结束符
    pre_end = re.compile('。|！|？')
    pre_num = re.compile('([０-９]+(·|．|／)[０-９]+)|([０-９]+)')
    pre_ch_num = re.compile('[一二三四五六七八九十百千万亿]+')

    for (num, line) in enumerate(input_pointer):
        # pre-process on this sentence
        line = "<BOS> " + line
        line = pre_end.subn("<EOS> <BOS>", line)[0]
        line = pre_num.subn("<n>", line)[0]
        line = pre_ch_num.subn("<N>", line)[0]
        # split the sentence
        words = re.findall("\S+", line)
        # statistic
        count += Counter(zip(words, islice(words, 1, None)))
        for item in words:
            word_list.add(item)

    input_pointer.close()
    del count[('<EOS>', '<BOS>')]
    # save data
    saving_data(count, word_list)


def load_counting():
    fq = open("count.data", "rb")
    count = pickle.load(fq)
    fq.close()
    return count


def load_word_list():
    fq = open("word.data", "rb")
    word_list = pickle.load(fq)
    fq.close()
    return word_list


def load_turing_data():
    fq = open("turing.data", "rb")
    turing_probability = pickle.load(fq)
    fq.close()
    return turing_probability


def fmm_segment(line, word_dict):
    '''
    use fmm to set sentence

    利用前向最大匹配算法进行句子切分，窗口最大长度为8，未出现过的以一个字为一个词进行切分
    @param line: 要进行切分的句子
    @param word_dict: 词典
    @return: 切分完的句子，存储在list 中
    '''
    window_size = 12
    if len(line) < 12:
        window_size = 9
    words = []
    idx = 0
    # fmm
    while idx < len(line):
        matched = False
        # size from window_size to 1
        for i in range(window_size, 0, -1):
            sub_str = line[idx: idx+i]
            if sub_str in word_dict:
                words.append(sub_str)
                matched = True
                idx += i
                break
        # only one
        if not matched:
            i = 1
            words.append(line[idx])
            idx += 1

    return words


def bmm_segment(line, word_dict):
    '''
    use bmm to set sentence

    利用后向最大匹配算法进行句子切分，窗口最大长度为8，未出现过的以一个字为一个词进行切分
    @param line: 要进行切分的句子
    @param word_dict: 词典
    @return: 切分完的句子，存储在list 中
    '''
    window_size = 12
    if len(line) < 12:
        window_size = 9
    words = []
    idx = len(line)
    # bmm
    while idx > 0:
        matched = False
        #size from window_size to 1
        for i in range(window_size, 0, -1):
            sub_str = line[idx-i: idx]
            if sub_str in word_dict:
                words.append(sub_str)
                matched = True
                idx -= i
                break
        #only one
        if not matched:
            i = 1
            words.append(line[idx-1])
            idx -= 1

    words.reverse()
    return words


def calculate_score(fmm_list, bmm_list, fmm_i, fmm_index, bmm_i, bmm_index, turing_p, word_dict, word_pair):
    fmm_p = 1
    bmm_p = 1
    for i in range(fmm_i, fmm_index):
        if fmm_list[i-1] in word_dict and fmm_list[i] in word_dict:
            fmm_p *= turing_p[word_pair[(fmm_list[i-1], fmm_list[i])]]
        else:
            fmm_p = 0

    for i in range(bmm_i, bmm_index):
        if bmm_list[i-1] in word_dict and bmm_list[i] in word_dict:
            bmm_p *= turing_p[word_pair[(bmm_list[i-1], bmm_list[i])]]
        else:
            bmm_p = 0
    if fmm_p > bmm_p :
        return fmm_list[fmm_i: fmm_index]
    else:
        return bmm_list[bmm_i: bmm_index]



def find_max_probability(fmm_list, bmm_list, turing_p, word_dict, word_pair):
    '''
    对前向后向的结果找到一个概率最大的组合

    根据已有的Turing平滑数据进行计算，返回一个具有最大概率的切分，采用局部最优的方法
    @param fmm_list: 前向切分得到的list
    @param bmm_list: 后向切分得到的list
    @param turing_p: 平滑后的概率分布
    @return: 返回带有粗糙的句子，之后还要结果替换和切除前部多余字符
    '''
    final_list = list()
    if fmm_list == bmm_list:
        text = " ".join(fmm_list)
    else:
        fmm_i = 0
        bmm_i = 0
        for i in range(0, len(fmm_list)):
            for j in range(bmm_i, len(bmm_list)):
                if fmm_list[i] == bmm_list[j] and  abs(i-j) < 5:
                    final_list += calculate_score(fmm_list, bmm_list, fmm_i, i, bmm_i, j, turing_p, word_dict, word_pair)
                    fmm_i = i
                    bmm_i = j
                    break
        final_list += calculate_score(fmm_list, bmm_list, fmm_i, len(fmm_list), bmm_i, len(bmm_list), turing_p, word_dict, word_pair)

        text = " ".join(final_list)
        # print(text)

    return text


def roll_back(final_line, end_mark, num_mark, ch_num_mark):
    '''
    恢复原来的被替换的标记，去除头部增加的前缀

    @param final_line: 根据最大概率 bi-gram 匹配出的结果
    @param end_mark: 被替换的句子结束符
    @param num_mark: 被替换的数字符号
    @return: 返回目标结果
    '''
    pre_end = re.compile('<EOS> +<BOS>')
    pre_num = re.compile('<n>')
    pre_ch_num = re.compile('<N>')
    for item in end_mark:
        final_line = pre_end.sub(item, final_line, 1)

    for item in num_mark:
        if item[0] != "":
            final_line = pre_num.sub(item[0], final_line, 1)
        else:
            final_line = pre_num.sub(item[2], final_line, 1)

    for item in ch_num_mark:
        final_line = pre_ch_num.sub(item, final_line, 1)

    return final_line[8:]


def segment(word_pair, word_dict, turing_probability):
    '''
    对指定文本进行切分

    根据传入的训练集得出的参数对指定文本进行切分，采用前向后向匹配进行粗切分，采用 bi-gram 进行消歧
    在进行切分前分别对数字和标点符号进行一定的预处理
    @param word_pair: bi-gram 计数
    @param word_dict: training data 中出现的 words
    @param turing_probability: good turing 计算结果
    @return: 无返回
    '''
    input_pointer = codecs.open("corpus_for_ass2test.txt", "r", "GBK")
    output_pointer = codecs.open("2011211672.txt", "w", "GBK")
    output_pointer.close()

    # 对标点和数字进行预处理，正则实现
    pre_end = re.compile('。|！|？')
    pre_num = re.compile('([０-９]+(·|．|／)[０-９]+)|([０-９]+)')
    pre_ch_num = re.compile('[一二三四五六七八九十百千万亿]+')
    pre_cut = re.compile('\s')

    # 对每一行进行处理
    for (num, line) in enumerate(input_pointer):
        # print(line)
        line = pre_cut.subn("", line)[0]
        # 将被替换的东西保存，便于最后的恢复
        end_mark = pre_end.findall(line)
        num_mark = pre_num.findall(line)
        ch_num_mark = pre_ch_num.findall(line)
        # 每一行前面增加一个 "<BOS> "
        line = "<BOS> " + line
        # 进行预处理替换
        line = pre_end.subn("<EOS> <BOS>", line)[0]
        line = pre_num.subn("<n>", line)[0]
        line = pre_ch_num.subn("<N>", line)[0]
        # use fmm and bmm to do segmentation
        fmm_list = fmm_segment(line, word_dict)
        bmm_list = bmm_segment(line, word_dict)

        seg_line = find_max_probability(fmm_list, bmm_list, turing_probability, word_dict, word_pair)

        # replace <EOS> <BOS> and <num>
        final_line = roll_back(seg_line, end_mark, num_mark, ch_num_mark)
        # output
        output_pointer = codecs.open("2011211672.txt", "a", "GBK")
        output_pointer.write(final_line + os.linesep)
        output_pointer.close()

    input_pointer.close()


if __name__ == "__main__":
    # init statistic
    # uncomment the following code to start statistic step
    # pre_counting()

    # load data
    statistic_pair = load_counting()
    statistic_dict = load_word_list()

    # calculate good-turing data
    # uncomment the following to calculate turing-good probability
    # good_turing(statistic_pair, statistic_dict)

    turing_probability = load_turing_data()

    # segment
    segment(statistic_pair, statistic_dict, turing_probability)