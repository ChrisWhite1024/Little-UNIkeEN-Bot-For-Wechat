import torch

class Config:
    '''
    数据集相关
    '''
    corpus_data_path = 'corpus/processed.pth' 
    shuffle = True
    #load_checkpoint = 'model_save/checkpoint_0509_1437.pth'
    load_checkpoint = None
    max_input_length = 50 #输入的最大句子长度
    max_generate_length = 20 #生成的最大句子长度
    '''
    训练超参数
    '''
    dim_embedding = 256 # 词嵌入维数
    num_layer = 2 # Encoder-Decoder中RNN的层数
    hidden_size = 256 # 隐藏层大小
    batch_size = 2048
    encoder_lr = 1e-3 # encoder学习率
    decoder_lr = 5e-3 # decoder学习率
    grad_clip = 50.0 # 梯度裁剪
    teacher_forcing_ratio = 1.0 # teacher_forcing的比例
    '''
    训练周期相关
    '''
    num_epoch = 6000
    save_epoch = 1000
    '''
    设备相关
    '''
    is_cuda = torch.cuda.is_available()
    device = "cuda:0" if is_cuda else "cpu" 