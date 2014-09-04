__author__ = 'Damcy'
# Copyright (c) 2014年 Damcy. All rights reserved.
# e-mail: stmayue@gmail.com
# Filename: test.py
import codecs
import os
import re
import pickle
from itertools import islice
from collections import Counter

# text1 = "据 世界 旅游 组织 公布 的 数字 ？ 去年 旅游 收入 最 多 的 国家 仍然 是 美国 ！ 为 ７５０·５６亿 美元 ， 比 １９／９６年 增加 ７·３６％ 。"
# text2 = "这 就 是 翟 俊杰 和 剧组 人员 ， 顶 着 １９９７年 酷暑 在 炼钢炉 前 拍 出 的 《 挺立 潮头 》 。 李 佩甫 编剧 ， 张 连文 、 姜 黎黎 主演 。 （ 西文 ）"
#
# text1 = "<BOS> " + text1
# text2 = "<BOS> " + text2
#
# pre_end = re.compile('。|！|？')
# text1 = pre_end.subn("<EOS> <BOS>", text1)[0]
# text2 = pre_end.subn("<EOS> <BOS>", text2)[0]
#
# pre_num = re.compile('([０-９]+(·|．|／)[０-９]+)|([０-９]+)')
# text1 = pre_num.subn("<num>", text1)[0]
# text2 = pre_num.subn("<num>", text2)[0]
#
# words1 = re.findall("\S+", text1)
# words2 = re.findall("\S+", text2)
# print(text1)
# print(text2)
# temp = Counter()
# temp += Counter(zip(words1, islice(words1, 1, None)))+Counter(zip(words2, islice(words2, 1, None)))
# del temp[('<EOS>', '<BOS>')]
# print(temp)
# z = temp.items()
# print(z)
# for pair in temp:
#     print("%s %s" % pair, temp[pair])

# fq = open("word.data", "rb")
# word_list = pickle.load(fq)
# fq.close()
#
# max = 0
# for item in word_list:
#     if len(item) >= max and len(item) < 9:
#         max = len(item)
#         print(item)
# print(max)

# a = ['aaa', 'aaaa', 'aaaaa']
# b = ['aaa', 'aa', 'aa', 'aaaaa']
#
# temp_a = set(a)
# temp_b = set(b)
# temp_c = temp_a & temp_b
#
# c = list(temp_c)
#
# print(c)
