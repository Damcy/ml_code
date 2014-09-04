import re
import codecs
import pickle
from collections import Counter


def load_b():
	fq = open("b_dict.data", "rb")
	global b_dict
	b_dict = pickle.load(fq)
	fq.close()


def load_tag_list():
	fq = open("tag_list.data", "rb")
	global tag_list
	tag_list = pickle.load(fq)
	fq.close()


def deal_words(line_word):
	for item in tag_list:
		for i in range(0, len(line_word)):
			if not b_dict[item].get(line_word[i], 0):
				b_dict[item][line_word[i]] = 0.000001


def normalization(my_dict, total):
	for item in my_dict:
		my_dict[item] /= total

	return my_dict


def get_dict_sum(my_dict):
	result = 0
	for item in my_dict:
		result += my_dict[item]

	return result


def save_b_dict():
	fq = open("b_dict_new.data", "wb")
	pickle.dump(b_dict, fq)
	fq.close()
	for item in b_dict:
		print(len(b_dict[item]))
	print(len(b_dict))


def main():
	load_b()
	load_tag_list()
	input_pointer = codecs.open("EM_after.txt", "r", "GBK")
	for (num, line) in enumerate(input_pointer):
		line_word = re.findall("\S+", line)
		deal_words(line_word)

	input_pointer.close()
	for item in b_dict:
		total = get_dict_sum(b_dict[item])
		b_dict[item] = normalization(b_dict[item], total)
	save_b_dict()


if __name__ == "__main__":
	main()
