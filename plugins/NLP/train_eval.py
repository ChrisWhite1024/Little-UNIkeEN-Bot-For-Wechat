import re
from tarfile import ENCODING
import time
import random
import jieba
import torch
import logging
import torch.nn as nn
from torchnet import meter
from model import Encoder_RNN, Decoder_RNN
from dataload import get_dataloader
from config import Config
from tqdm import tqdm
from greedysearch import GreedySearchDecoder
jieba.setLogLevel(logging.INFO) #关闭jieba输出信息

def maskNLLLoss(inp, target, mask):
    '''
    inp: shape [batch_size,voc_length]
    target: shape [batch_size] 经过view ==> [batch_size, 1] 这样就和inp维数相同, 可以用gather
        target作为索引,在dim=1上索引inp的值,得到的形状同target [batch_size, 1]
        然后压缩维度,得到[batch_size], 取负对数后
        选择那些值为1的计算loss, 并求平均, 得到loss
        故loss实际是batch_size那列的均值, 表示一个句子在某个位置(t)上的平均损失值
        故nTotal表示nTotal个句子在某个位置上有值
    mask: shape [batch_size]
    loss: 平均一个句子在t位置上的损失值
    '''
    nTotal = mask.sum() #padding是0，非padding是1，因此sum就可以得到词的个数
    crossEntropy = -torch.log(torch.gather(inp, 1, target.view(-1, 1)).squeeze(1))
    loss = crossEntropy.masked_select(mask).mean()
    return loss, nTotal.item()

def train_by_batch(sos, conf, data, encoder_optimizer, decoder_optimizer, encoder, decoder):
    #清空梯度
    encoder_optimizer.zero_grad()
    decoder_optimizer.zero_grad()
    #处理一个batch数据
    inputs, targets, mask, input_lengths, max_target_length, indexes = data
    inputs = inputs.to(conf.device)
    targets = targets.to(conf.device)
    mask = mask.to(conf.device)
    input_lengths =  input_lengths.to(conf.device)
    # 初始化变量
    loss = 0
    print_losses = []
    n_totals = 0

    #forward计算
    '''
    inputs: shape [max_seq_len, batch_size]
    input_lengths: shape [batch_size]
    encoder_outputs: shape [max_seq_len, batch_size, hidden_size]
    encoder_hidden: shape [num_layers*num_directions, batch_size, hidden_size]
    decoder_input: shape [1, batch_size]
    decoder_hidden: decoder的初始hidden输入,是encoder_hidden取正方向
    '''
    encoder_outputs, encoder_hidden = encoder(inputs, input_lengths)
    decoder_input = torch.LongTensor([[sos for _ in range(conf.batch_size)]])
    decoder_input = decoder_input.to(conf.device)
    decoder_hidden = encoder_hidden[:decoder.num_layer]

    # 确定是否teacher forcing
    use_teacher_forcing = True if random.random() < conf.teacher_forcing_ratio else False

    '''
    一次处理一个时刻，即一个字符
    decoder_output: [batch_size, voc_length]
    decoder_hidden: [decoder_num_layers, batch_size, hidden_size]
    如果使用teacher_forcing,下一个时刻的输入是当前正确答案，即
    targets[t] shape: [batch_size] ==> view后 [1, batch_size] 作为decoder_input
    '''
    if use_teacher_forcing:
        for t in range(max_target_length):
            decoder_output, decoder_hidden = decoder(
                decoder_input, decoder_hidden, encoder_outputs
            )
            # 使用teacher_forcing,下一个时刻的输入是当前正确答案
            decoder_input = targets[t].view(1, -1)
            
            # 计算累计的loss
            '''
            每次迭代,
            targets[t]: 一个batch所有样本指定位置(t位置)上的值组成的向量，shape [batch_size]
            mask[t]: 一个batch所有样本指定位置(t位置)上的值组成的向量, 值为1表示此处未padding
            decoder_output: [batch_size, voc_length]
            '''
            mask_loss, nTotal = maskNLLLoss(decoder_output, targets[t], mask[t])
            mask_loss = mask_loss.to(conf.device)
            loss += mask_loss
            '''
            这里loss在seq_len方向迭代进行累加, 最终得到一个句子在每个位置的损失均值之和
            总结:  mask_loss在batch_size方向累加,然后求均值,loss在seq_len方向进行累加
            即: 一个batch的损失函数: 先计算所有句子在每个位置的损失总和,再除batch_size
            这里的loss变量用于反向传播，得到的是一个句子的平均损失
            '''
            print_losses.append(mask_loss.item() * nTotal)
            n_totals += nTotal
    else:
        for t in range(max_target_length):
            decoder_output, decoder_hidden = decoder(
                decoder_input, decoder_hidden, encoder_outputs
            )
            # 不是teacher forcing: 下一个时刻的输入是当前模型预测概率最高的值
            _, topi = decoder_output.topk(1)
            decoder_input = torch.LongTensor([[topi[i][0] for i in range(conf.batch_size)]])
            decoder_input = decoder_input.to(conf.device)
            # 计算累计的loss
            mask_loss, nTotal = maskNLLLoss(decoder_output, targets[t], mask[t])
            loss += mask_loss
            print_losses.append(mask_loss.item() * nTotal)
            n_totals += nTotal

    #反向传播
    loss.backward()

    # 对encoder和decoder进行梯度裁剪
    _ = torch.nn.utils.clip_grad_norm_(encoder.parameters(), conf.grad_clip)
    _ = torch.nn.utils.clip_grad_norm_(decoder.parameters(), conf.grad_clip)

    #更新参数
    encoder_optimizer.step()
    decoder_optimizer.step()
    #这里是batch中一个位置(视作二维矩阵一个格子)的平均损失
    return sum(print_losses) / n_totals 

def train(**kwargs):

    conf = Config()
    # 加载数据
    dataloader = get_dataloader(conf)
    _data = dataloader.dataset._data
    word2ix = _data['word2ix']
    sos = word2ix.get(_data.get('sos'))
    len_vocab = len(word2ix)

    # 模型
    encoder = Encoder_RNN(conf, len_vocab)
    decoder = Decoder_RNN(conf, len_vocab)
    if conf.load_checkpoint:
        checkpoint = torch.load(conf.load_checkpoint) 
        encoder.load_state_dict(checkpoint['encoder'])
        decoder.load_state_dict(checkpoint['decoder'])
    encoder.to(conf.device)
    decoder.to(conf.device)
    encoder.train()
    decoder.train()

    encoder_optimizer = torch.optim.Adam(encoder.parameters(), lr=conf.encoder_lr)
    decoder_optimizer = torch.optim.Adam(decoder.parameters(), lr=conf.decoder_lr)
    if conf.load_checkpoint:
        checkpoint = torch.load(conf.load_checkpoint) 
        encoder_optimizer.load_state_dict(checkpoint['encoder_opt'])
        decoder_optimizer.load_state_dict(checkpoint['decoder_opt']) 

    for epoch in tqdm(range(conf.num_epoch)):
        tot_loss = 0
        ii = 1
        for data in dataloader:
            loss = train_by_batch(sos, conf, data, encoder_optimizer, decoder_optimizer, encoder, decoder)
            tot_loss += loss
            ii += 1
        #print(f"epoch:{epoch}, avg_loss:{float(tot_loss/ii)}")

        if epoch % conf.save_epoch:
            checkpoint_path = 'model_save/checkpoint_{time}.pth'.format(time=time.strftime('%m%d_%H%M'))
            torch.save({
                'encoder': encoder.state_dict(),
                'decoder': decoder.state_dict(),
                'encoder_opt': encoder_optimizer.state_dict(),
                'decoder_opt': decoder_optimizer.state_dict(),
            }, checkpoint_path)

def eval(input_sentence):
    conf = Config()
    # 加载数据
    dataloader = get_dataloader(conf)
    _data = dataloader.dataset._data
    word2ix,ix2word = _data['word2ix'], _data['ix2word']
    sos = word2ix.get(_data.get('sos'))
    eos = word2ix.get(_data.get('eos'))
    unk = word2ix.get(_data.get('unk'))
    len_vocab = len(word2ix)

    encoder = Encoder_RNN(conf, len_vocab)
    decoder = Decoder_RNN(conf, len_vocab)

    checkpoint = torch.load(conf.load_checkpoint, map_location=lambda s, l: s)
    encoder.load_state_dict(checkpoint['encoder'])
    decoder.load_state_dict(checkpoint['decoder'])

    with torch.no_grad():
        #切换模式
        encoder = encoder.to(conf.device)
        decoder = decoder.to(conf.device)
        encoder.eval()
        decoder.eval()
        #定义seracher
        searcher = GreedySearchDecoder(encoder, decoder)

        cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]") #分词处理正则
        input_seq = jieba.lcut(cop.sub("",input_sentence)) #分词序列
        input_seq = input_seq[:conf.max_input_length] + ['</EOS>']
        input_seq = [word2ix.get(word, unk) for word in input_seq]
        tokens = generate(input_seq, searcher, sos, eos, conf)
        output_words = ''.join([ix2word[token.item()] for token in tokens])
        print('BOT: ', output_words)


def generate(input_seq, searcher, sos, eos, opt):
    #input_seq: 已分词且转为索引的序列
    #input_batch: shape: [1, seq_len] ==> [seq_len,1] (即batch_size=1)
    input_batch = [input_seq]
    input_lengths = torch.tensor([len(seq) for seq in input_batch])
    input_batch = torch.LongTensor([input_seq]).transpose(0,1)
    input_batch = input_batch.to(opt.device)
    input_lengths = input_lengths.to(opt.device)
    tokens, scores = searcher(sos, eos, input_batch, input_lengths, opt.max_generate_length, opt.device)
    return tokens

if __name__ == "__main__":
    #eval("早安")
    train()