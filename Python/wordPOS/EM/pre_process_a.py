import re
import pickle

def load_a():
	fq = open("a_dict.data", "rb")
	global a_dict
	a_dict = pickle.load(fq)
	fq.close()


def load_tag_list():
	fq = open("tag_list.data", "rb")
	global tag_list
	tag_list = pickle.load(fq)
	fq.close()


def normalization(my_dict, total):
	for item in my_dict:
		my_dict[item] /= total
	
	return my_dict


def get_dict_sum(my_dict):
	result = 0
	for item in my_dict:
		result += my_dict[item]

	return result


def deal_with_tag():
	for item_1 in tag_list:
		for item_2 in tag_list:
			if not a_dict[item_1].get(item_2, 0):
				a_dict[item_1][item_2] = 0.000001


def main():
	load_a()
	load_tag_list()
	deal_with_tag()
	for item in tag_list:
		total = get_dict_sum(a_dict[item])
		a_dict[item] = normalization(a_dict[item], total)
	fq = open("a_dict_new.data", "wb")
	pickle.dump(a_dict, fq)
	fq.close()


if __name__ == "__main__":
	main()
