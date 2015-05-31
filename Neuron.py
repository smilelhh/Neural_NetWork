# -*- coding: utf8 -*-
# Copyright © 2015-2016 Jay Sinco -v python2.6

import random
import math
import matplotlib.pyplot as plt

#import pickle

def rand(a, b):
    ''' 生成[a,b)内的随机数 '''
    return (b - a)*random.random() + a

def makeMatrix(I, J, fill=0.0):
    ''' 生成 I*J 大小的矩阵 '''    
    return [[fill]*J for i in range(I)]

def sigmoid(x):
    ''' 激活函数 '''
    #return math.tanh(x)
    #return 1.0/(1 + math.exp(-x))
    return 0.5 * (1 + math.tanh(0.5 * x))

class Neuron:
    def __init__(self, ni, nh, no, A = 0.5, B = 0.1):
        ''' 输入层，隐层，输出层的初始化 '''
        # 网络学习率和动量因子设定
        self.A = A
        self.B = B
        # 考虑到神经元阈值，输入层+1，且应初始化为 1
        self.ni = ni + 1   
        self.nh = nh
        self.no = no    
        # 设置各层的存储向量
        self.ai = [1.0] * self.ni
        self.ah = [1.0] * self.nh
        self.ao = [1.0] * self.no
        # 最后建立动量因子矩阵
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)
        # 设置权值矩阵
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        # 初始化权值矩阵
        for i in range(self.ni):
            for j in range(self.nh):
                for k in range(self.no):
                    self.wi[i][j] = rand(-0.2, 0.2)    
                    self.wo[j][k] = rand(-2.0, 2.0)
                    
    def runfront(self, inputs):
        ''' 正向传播，inputs为单个训练样本输入'''
        if len(inputs) != self.ni - 1:
            raise ValueError("输入节点数错误")
        # 计算输入层输出
        for i in range(self.ni - 1):
            self.ai[i] = inputs[i]
        # 计算隐层输出
        for j in range(self.nh):
            self.ah[j] = sigmoid(sum([self.ai[i]*self.wi[i][j]  for i in range(self.ni)]))
        # 计算输入层输出
        for k in range(self.no):
            self.ao[k] = sigmoid(sum([self.ah[j]*self.wo[j][k] for j in range(self.nh)]))
        return self.ao
     
    def runback(self, outputs):
        ''' 反向传播, outputs为训练样本期望输出 '''
        Error = 0.0   # 网络误差
        if len(outputs) != self.no:
            raise ValueError('输出节点数错误')
        # 计算输出层误差
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            reo = self.ao[k]   # 实际输出
            wano = outputs[k]  # 期望输出
            output_deltas[k] = (wano - reo) * (1 - reo**2)
            Error += 0.5 * (wano - reo)**2   # 计算整体网络误差             
        # 计算隐层误差
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            reo = self.ah[j]
            error = 0.0
            for k in range(self.no):
                error +=  output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = (1 - reo**2) * error
        # 更新输出层权值
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] += self.A * change + self.B * self.co[j][k]
                self.co[j][k] = change
        # 更新隐层权重
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j] * self.ai[i]
                self.wi[i][j] += self.A * change  + self.B * self.ci[i][j]
                self.ci[i][j] = change
        return Error 
    
    def train(self, dataSet, iteration):
        ''' 训练网络，打印训练样本的整体误差 '''
        for i in range(iteration):
            All_Error = 0.0
            for data in dataSet:
                self.runfront(data[0])
                All_Error += self.runback(data[1])               
            Logger.append(All_Error)
            if i%100 == 0:
                print i, "Iter's error: ", All_Error                
        print "样本已完成%d次迭代训练"%iteration,"下面开始测试\n"

            

# 构造神经网络            
N_In = 25   # 输入层神经元数量
N_Out = 3    # 输出层神经元数量
N_Hidden = 8   # 隐层神经元数量 
N_Train = 1000    # 训练次数 
Alpha = 0.8    # 学习常数 
Belta = 0.5   # 动量因子  
NN = Neuron(N_In, N_Hidden, N_Out, Alpha, Belta)

Logger = []  # 记录迭代中的误差变化

# 从文件中获取训练数据
#Train_File = open('Train_data.txt', 'r')
#Train_Set = []
#for i in range(N_Out):
#    Train_Set.append(pickle.load(Train_File))
#Train_File.close()
#print Train_Set

Train_Set = [
    [[1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1], [1, 0, 0]],  # 燕子图案
    [[1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1], [0, 1, 0]],  # 箭头
    [[1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1], [0, 0, 1]]   # 方块
]

# 训练           
NN.train(Train_Set, N_Train)

# 画误随迭代次数差变化图
plt.plot(Logger)
plt.xlim(0,150)
plt.xlabel("Iteration-Count")
plt.ylabel("Error")

plt.show()

# 测试
def test(n, s):
    res = NN.runfront(Train_Set[n][0])
    ide = Train_Set[n][1]
    print "** 测试 <%s> 图案"%(s)
    print "  -实际输出 => [", ", ".join(["%.3f"%d for d in res ]), "]"
    print "  -理想输出 => [", ", ".join(["%.3f"%d for d in ide ]), "]"
    print

test(0, "燕子")
test(1, "箭头")
test(2, "方块")






