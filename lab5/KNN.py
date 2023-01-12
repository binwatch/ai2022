import numpy as np
import operator as op

def classify0(in_x, data_set, labels, k):
    m = data_set.shape[0] # 返回 data_set 的行数，即已知数据集中所有点的数量
    diff_mat = np.tile(in_x, (m, 1)) - data_set # 行向量方向上将 in_x 复制m 次，然后和 data_set 矩阵做相减运算
    sq_diff_mat = diff_mat**2 # 减完后对每个数做平方运
    sq_distances = sq_diff_mat.sum(axis=1) # 平方后按行求和，axis=0 表示列相加，axis=1 表示行相加
    distances = sq_distances**0.5 # 开平方计算欧式距离
    sorted_dist_indices = distances.argsort() # 对距离从小到大排序，argsort 返回数组值从小到大的索引值
    class_count = {} # 类别、投票次数的字典，key 为类别，value 为投票次数
    for i in range(k):
        voteIlabel = labels[sorted_dist_indices[i]] # 取出第 i 近的元素对应的类别
        class_count[voteIlabel] = class_count.get(voteIlabel, 0) + 1 # 对类别次数进行累加
    sorted_class_count = sorted(class_count.items(), key=op.itemgetter(1), reverse=True) # 根据字典的值从大到小进行排序
    return sorted_class_count[0][0] # 返回次数最多的类别，即所要分类的类别

if __name__ == '__main__':
    data_set = np.array([[250, 100], [270, 120], [111, 230], [130, 260], [200, 80], [70, 190]])
    labels = ["理科生", "理科生", "文科生", "文科生", "理科生", "文科生"]
    in_x = [105, 210]
    print(classify0(in_x, data_set, labels, 3))