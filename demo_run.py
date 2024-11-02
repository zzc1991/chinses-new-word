import os
import time

import jieba
from modelhnj import TrieNode
from utils import get_stopwords, load_dictionary, generate_ngram, save_model, load_model
from config import basedir


def load_data(filename, stopwords):
    data = []
    with open(filename, 'r',encoding='utf-8') as f:
        for line in f:
            word_list = [x for x in jieba.cut(line.strip(), cut_all=False) if x not in stopwords]
            data.append(word_list)
    return data


def load_data_2_root(data):
    for word_list in data:
        ngrams = generate_ngram(word_list, 3)
        for d in ngrams:
            root.add(d)

if __name__ == "__main__":
    T1 = time.time()
    root_name = basedir + "/data/root.pkl"
    stopwords = get_stopwords()
    if os.path.exists(root_name):
        root = load_model(root_name)
    else:
        dict_name = basedir + '/data/dict.txt'
        word_freq = load_dictionary(dict_name)
        root = TrieNode('*', word_freq)
        save_model(root, root_name)

    # 加载新的文章
    filename = 'data/demo100000.txt'
    data = load_data(filename, stopwords)
    # 将新的文章插入到Root中
    load_data_2_root(data)

    # 定义取TOP5个
    topN = 5
    result, add_word = root.find_word(topN)
    # 如果想要调试和选择其他的阈值，可以print result来调整
    # print("\n----\n", result)
    T2 = time.time()
