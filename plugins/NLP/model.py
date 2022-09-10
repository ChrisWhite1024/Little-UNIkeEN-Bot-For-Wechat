from multiprocessing import context
from turtle import dot
from unicodedata import bidirectional
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.utils as utils

class Encoder_RNN(nn.Module):
    def __init__(self, conf, len_vocab):
        super(Encoder_RNN, self).__init__()
        # RNN层数与隐藏层大小
        self.num_layer = conf.num_layer
        self.hidden_size = conf.hidden_size
        # emb的输入为字典长度（词的个数）
        self.embedding = nn.Embedding(len_vocab, conf.dim_embedding)
        # 双层GRU
        self.gru = nn.GRU(
            input_size = conf.dim_embedding,
            hidden_size = self.hidden_size,
            num_layers = self.num_layer,
            bidirectional = True # 使用双向GRU
        )

    def forward(self, input_seq, input_lengths, hidden = None): # 初始hidden为空
        '''
        input_seq:输入序列
            size: [max_seq_len, batch_size]
        input_lengths:输入序列长度,某一batch内每个句子的长度列表
            size: [batch_size]
        '''
        # 词嵌入
        embedded = self.embedding(input_seq)
        '''
        embedded:词嵌入处理后
            size: [max_seq_len, batch_size, dim_embedding]
        '''
        # 按照序列长度列表对矩阵进行压缩,加快RNN的计算效率
        packed_data = utils.rnn.pack_padded_sequence(embedded, input_lengths)
        output, hidden = self.gru(packed_data, hidden)
        # 解压缩为定长序列矩阵
        output, _ = utils.rnn.pad_packed_sequence(output)
        '''
        hidden:隐藏层,初始值为None
            size: [num_layers*num_directions, batch_size, hidden_size]
            双向GRU,其第一个维度为不同方向的叠加
        output:输出层
            size: [max_seq_len, batch_size, num_directions*hidden_size]
        '''
        # 对前后两个方向求和输出
        output = output[:,:,:self.hidden_size]+output[:,:,self.hidden_size:]
        '''
        output.size->[max_seq_len, batch_size, hidden_size]
        '''
        return output, hidden


class Decoder_RNN(nn.Module):
    def __init__(self, conf, len_vocab):
        super(Decoder_RNN, self).__init__()
        # RNN层数和隐藏层大小
        self.num_layer = conf.num_layer
        self.hidden_size = conf.hidden_size
        # emb的输入为字典长度（词的个数）
        self.embedding = nn.Embedding(len_vocab, conf.dim_embedding)
        # GRU
        self.gru = nn.GRU(
            input_size = conf.dim_embedding,
            hidden_size = self.hidden_size,
            num_layers = self.num_layer,
        )
        # concat层与输出层
        self.concat = nn.Linear(self.hidden_size*2, self.hidden_size)
        self.out = nn.Linear(self.hidden_size, len_vocab)

    def forward(self, input, hidden, encoder_hiddens):
        '''
        input:输入
            decoder逐字生成,后一个时间步接受前一个时间步生成的字。第一个时间步接受句子开始的符号
            即接受input=开始符索引
            shape:[1, batch_size]
        '''
        # 词嵌入
        embedded = self.embedding(input)
        '''
        embedded:词嵌入处理后
            size: [1, batch_size, dim_embedding]
        '''
        # RNN
        output, hidden = self.gru(embedded, hidden)
        '''
        hidden:隐藏层,最早传入的是encoder最后时刻的输出层,encoder_hidden的正向部分
            size: [num_layers, batch_size, hidden_size]
            双向GRU,其第一个维度为不同方向的叠加
        output:输出层
            size: [max_seq_len, batch_size, hidden_size]
        '''
        # dot方式计算Attention
        '''
        encoder_outputs:
            encoder所有时间步的hidden输出
            shape: [max_seq_len, batch_size, hidden_size]
        '''
        dot_score = torch.sum(output* encoder_hiddens, dim=2).t()
        dot_score = F.softmax(dot_score, dim=1).unsqueeze(1)
        '''
        dot_score: attention的得分
            shape: [max_seq_len, batch_size]
            转置->[batch_size, max_seq_len]
            增加维度->[batch_size, 1, max_seq_len]
        '''
        # 批量相乘，形成context
        context = dot_score.bmm(encoder_hiddens.transpose(0,1))
        context = context.squeeze(1)
        '''
        context:
            shape: [batch_size, hidden_size]
        '''
        output = output.squeeze(0) # [batch_size, hidden_size]
        # 拼接output和context，通过线性层变为单层
        concat_input = torch.cat((output, context), 1)
        concat_output = torch.tanh(self.concat(concat_input)) 
        # 输出与softmax归一化
        final_output = self.out(concat_output)
        final_output = F.softmax(final_output, dim=1)

        return final_output, hidden



        
        