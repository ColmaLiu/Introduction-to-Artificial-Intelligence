from numpy.random import rand
import mnist
from answerTree import *
import numpy as np

# 超参数
# TODO: You can change the hyperparameters here
num_tree = 50     # 树的数量
ratio_data = 0.7   # 采样的数据比例
ratio_feat = 0.5 # 采样的特征比例
hyperparams = {
    "depth":100, 
    "purity_bound":0.8,
    "gainfunc": gainratio
    } # 每颗树的超参数


def buildtrees(X, Y):

    """
    构建随机森林
    @param X: n*d, 每行是一个输入样本。 n: 样本数量， d: 样本的维度
    @param Y: n, 样本的label
    @return: List of DecisionTrees, 随机森林
    """
    # TODO: YOUR CODE HERE
    # 提示：整体流程包括样本扰动、属性扰动和预测输出
    trees=[]
    new_n=int(X.shape[0]*ratio_data)
    new_d=int(X.shape[1]*ratio_feat)
    for _ in range(num_tree):
        selected_data=np.random.choice(X.shape[0],size=new_n,replace=False)
        new_X=X[selected_data]
        new_Y=Y[selected_data]
        selected_feat=np.random.choice(X.shape[1],size=new_d,replace=False)
        root=buildTree(new_X,new_Y,selected_feat.tolist(),**hyperparams)
        trees.append(root)
    return trees 

def infertrees(trees, X):
    """
    随机森林预测
    @param trees: 随机森林
    @param X: n*d, 每行是一个输入样本。 n: 样本数量， d: 样本的维度
    @return: n, 预测的label
    """
    pred = [inferTree(tree, X)  for tree in trees]
    pred = list(filter(lambda x: not np.isnan(x), pred))
    upred, ucnt = np.unique(pred, return_counts=True)
    return upred[np.argmax(ucnt)]
