# Copyright (c) 2014 Damcy. All rights reserved.
# e-mail: stmayue@gmail.com
# Filename: HMM_EM.py

import re
import pickle
import os
import codecs
from collections import Counter


def find_max_ele(my_dict):
	max_pos = None
	max_value = float("-inf")
	for item in my_dict:
		if my_dict[item] > max_value:
			max_value = my_dict[item]
			max_pos = item

	return max_pos


def viterbi_tag(line_word, a, b, tags, pai):
	result_list = list()
	# init delta and psi
	delta = dict()
	psi = dict()
	for i in range(0, len(line_word)):
		delta[i] = dict()
		psi[i] = dict()
		for item in tags:
			delta[i][item] = float("-inf")
			psi[i][item] = 0
	for item in tags:
		delta[0][item] = pai[item] + b[item][line_word[i]]
	#viterbi
	for i in range(1, len(line_word)):
		for item_1 in tags:
			for item_2 in tags:
				if line_word[i] in words:
					temp = delta[i-1][item_2] + a[item_2][item_1]
				if temp > delta[i][item_1]:
					delta[i][item_1] = temp
					psi[i][item_1] = item_2
	# track back
	position = find_max_ele(delta[len(line_word) - 1])
	temp_list = list()
	for i in range(len(line_word)-1, -1, -1):
		temp_list.append(position)
		position = psi[i][position]
	temp_list = reverse()
	# return tagged list
	return temp_list
	

def baum_welch(a_dict, b_dict, tag_list):
	iter_mark = 1
	pai = dict()
	# 初始的概率值为取平均值，因为MLE预料中起一个为日期
	for tag in tag_list:
		pai[tag] = 1/len(tag_list)
	# 迭代
	iter_mark = 1
	while iter_mark:
		temp_mark = 1
		# t = 1处于Si的次数
		startstate = dict()
		# 由 i 转换到 j 的次数
		transition = dict()
		# 从Si转移出去的次数 
		transfrom = dict()
		# 处于Sj并且观察值为k的次数
		observation = dict()
		# 处于Si的次数
		state = dict()
		for i in tag_list:
			startstate[i] = 0
			transition[i] = dict()
			transfrom[i] = 0
			observation[i] = dict()
			state[i] = 0
			for j in tag_list:
				transition[i][j] = 0

		input_pointer = codecs.open("EM_after.txt", "r", "GBK")
		for (num, line) in enumerate(input_pointer):
			line_word = re.findall("\S+", line)
			if len(line_word) == 0:
				continue
			# line_tag = viterbi_tag(line_word, a_dict, b_dict, tag_list, pai)
			# 进行前向 后向计算并加入5个参数
			beta = dict()
			alpha = dict()
			gamma = dict()
			xi = dict()
			for i in range(0, len(line_word)):
				beta[i] = dict()
				alpha[i] = dict()
				gamma[i] = dict()
				if i != len(line_word) - 1:
					xi[i] = dict()
					for item in tag_list:
						xi[i][item] = dict()
			# update alpha
			for item in tag_list:
				alpha[0][item] = pai[item] * b_dict[item][line_word[0]]
			
			for i in range(1, len(line_word)):
				for item in tag_list:
					alpha[i][item] = 0
					for item_2 in tag_list:
						#print(i, item, item_2)
						alpha[i][item] += alpha[i-1][item_2] * a_dict[item_2][item]
					alpha[i][item] *= b_dict[item][line_word[i]]
			# update beta
			for item in tag_list:
				beta[len(line_word) - 1][item] = 1
			for i in range(len(line_word) - 2, -1, -1):
				for item_1 in tag_list:
					for item_2 in tag_list:
						#print(a_dict[item_1][item_2], beta[i+1][item_2])
						#print(b_dict[item_2][line_word[i+1]])
						beta[i][item_1] = beta[i].get(item_1, 0) + a_dict[item_1][item_2] * b_dict[item_2][line_word[i+1]] * beta[i+1][item_2]
			# update xi
			for i in range(0, len(line_word) - 1):
				frac = 0.0
				for item_1 in tag_list:
					for item_2 in tag_list:
						frac += alpha[i][item_1] * a_dict[item_1][item_2] * b_dict[item_2][line_word[i+1]] * beta[i+1][item_2]
				for item_1 in tag_list:
					for item_2 in tag_list:
						if not frac:
							xi[i][item_1][item_2] = 0
						else:
							xi[i][item_1][item_2] = alpha[i][item_1] * a_dict[item_1][item_2] * b_dict[item_2][line_word[i+1]] * beta[i+1][item_2] / frac
			# update gamma
			for i in range(0, len(line_word)):
				frac = 0.0
				for item in tag_list:
					frac += alpha[i][item] * beta[i][item]
				for item in tag_list:
					if not frac:
						gamma[i][item] = 0
					else:
						gamma[i][item] = alpha[i][item] * beta[i][item] / frac
			# 更新5个参数
			# update startstate
			for item in tag_list:
				startstate[item] = startstate.get(item, 0) + gamma[0][item]
			# update transition
			for item_1 in tag_list:
				for item_2 in tag_list:
					temp = 0
					for i in range(0, len(line_word)-1):
						temp += xi[i][item_1][item_2]
					transition[item_1][item_2] = transition[item_1].get(item_2, 0) + temp
			# update transfrom
			for item in tag_list:
				temp = 0
				for i in range(0, len(line_word)-1):
					temp += gamma[i][item]
				transfrom[item] = transfrom.get(item, 0) + temp
			# update observation
			for item in tag_list:
				for i in range(0, len(line_word)):
					observation[item][line_word[i]] = observation[item].get(line_word[i], 0) + gamma[i].get(item, 0)
			# update state
			for item in tag_list:
				for i in range(0, len(line_word)):
					#print(line_word[i], item)
					state[item] = state.get(item, 0) + gamma[i][item]
		input_pointer.close()
		# 计算新的π A B矩阵
		# π
		first_total = 0
		for item in tag_list:
			first_total += startstate.get(item, 0)
		for item in tag_list:
			pai[item] = startstate.get(item, 0) / first_total
		# A
		for item_1 in tag_list:
			for item_2 in tag_list:
				a_dict[item_1][item_2] = transition[item_1][item_2] / transfrom[item_1]
		# B
		for item_1 in b_dict:
			for item_2 in b_dict[item_1]:
				b_dict[item_1][item_2] = observation[item_1].get(item_2, 0) / state[item_1]
		# 如果每一个参数改变的幅度均小于一定的阈值则完成训练
#		if temp_mark:
#			print(iter_mark)
#			iter_mark = 0
#		else:
#			iter_mark += 1
		iter_mark -= 1
	fq = open("em_a.data", "wb")
	pickle.dump(a_dict, fq)
	fq.close()
	fq = open("em_b.data", "wb")
	pickle.dump(b_dict, fq)
	fq.close()
	fq = open("em_pai.data", "wb")
	pickle.dump(pai, fq)
	fq.close()


def load_a():
	# MLE中 词 转换为 tag 的概率，作为EM的初始值
	fq = open("a_dict_new.data", "rb")
	a_dict = pickle.load(fq)
	fq.close()
	return a_dict


def load_b():
	# MLE中 tag 之间转换概率，作为EM的初始值
	fq = open("b_dict_new.data", "rb")
	b_dict = pickle.load(fq)
	fq.close()
	return b_dict


def load_tag_list():
	# 训练样本中存在的tag集
	fq = open("tag_list.data", "rb")
	tag_list = pickle.load(fq)
	fq.close()
	return tag_list


def main():
	a_dict = load_a()
	b_dict = load_b()
	tag_list = load_tag_list()
	baum_welch(a_dict, b_dict, tag_list)


if __name__ == "__main__":
	main()
