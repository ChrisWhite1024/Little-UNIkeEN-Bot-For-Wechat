from concurrent.futures import process
import re
import jieba
import torch
import logging
jieba.setLogLevel(logging.INFO)

source_corpus_path = 'corpus/source.tsv' # 处理前原始数据集
save_corpus_path = 'corpus/processed.pth' # 处理后数据集
cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]") # 分词处理时正则筛选
unk = "</UNK>" # 未知字符标识符
eos = "</EOS>" # 句子结束符
sos = "</SOS>" # 句子起始符
pad = "</PAD>" # 句子填充符
max_voc_length = 10000 # 字典最大长度
min_word_freq = 10 # 计入字典的最小词频
max_sentence_len = 50 # 最大句长

def preprocess():
    print('start preprocessing...')
    data = []
    with open(source_corpus_path, encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            tmp = line.strip('\n').split('\t')
            sentences = []
            for value in tmp:
                value_p = cop.sub("", value)
                word_list = jieba.lcut(value_p)
                word_list = word_list[:max_sentence_len]+[eos]
                sentences.append(word_list)
            data.append(sentences)
    word_nums = {}
    # 统计词频
    for sentences in data:
        for sentence in sentences:
            for word in sentence:
                word_nums[word] = word_nums.get(word,0) + 1
    nums_list = sorted([(num, word) for word, num in word_nums.items()], reverse=True)
    words = [word[1] for word in nums_list[:max_voc_length] if word[0]>min_word_freq]
    words = [unk, sos, pad] + words
    word2index = {word: ix for ix, word in enumerate(words)}
    index2word = {ix: word for word, ix in word2index.items()}
    ix_corpus = [[[word2index.get(word, word2index.get(unk)) for word in sentence]
                        for sentence in sentences]
                        for sentences in data]
    processed_data={
        "corpus": ix_corpus,
        "word2ix": word2index,
        "ix2word": index2word,
        "unk": unk,
        "eos": eos,
        "sos": sos,
        "pad": pad
    }
    torch.save(processed_data, save_corpus_path)
    print('finish processing')

if __name__ == "__main__":
    preprocess()