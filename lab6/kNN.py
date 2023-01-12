import numpy as np
import operator as op
from os import listdir

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

def img2vector(filename): # 将图片文件转换成一个向量
    ret_vect = np.zeros((1, 1024)) # 创建一个 1024 个分量的 0 向量
    file = open(filename) # 打开文件
    for i in range(32):
        line_str = file.readline() # 读取文件的一行
        for j in range(32): # 对当前一行的向量添加到结果末尾
            ret_vect[0, 32*i + j] = int(line_str[j])
    return ret_vect

# if __name__ == '__main__':
#     np.set_printoptions(threshold=np.inf)
#     print(img2vector('./data/kNN_hand_writing/trainingDigits/0_0.txt'))

def load_train_data():
    hw_labels = []
    training_file_list = listdir("./data/kNN_hand_writing/trainingDigits") # 所有图片的文件名形成一个列表
    m = len(training_file_list)         # 返回训练集下 txt 文件数量
    training_mat = np.zeros((m, 1024))  # 初始化训练的 Mat 矩阵，测试集
    for i in range(m):      # 依次读取每个文件
        file_name_str = training_file_list[i]
        class_number = int(file_name_str.split('_')[0])     # 根据文件名获取分类数字
        hw_labels.append(class_number)      # 获得的类别添加到 hw_labels 中
        print("fileName %s class_number %s " % (file_name_str, class_number))
        training_mat[i, :] = img2vector('./data/kNN_hand_writing/trainingDigits/%s' % (file_name_str))  # 将每一个文件的 1x1024 数据存储到 training_mat
    return hw_labels, training_mat

def kNN_hand_written_test():
    error_count = 0.0       # 错误检测计数
    hw_labels, training_mat = load_train_data()
    test_file_list = listdir('./data/kNN_hand_writing/testDigits')
    m_test = len(test_file_list)    # 测试数据的数量
    for i in range(m_test):         # 从文件中解析出测试集的类别并进行分类测试
        file_name_str = test_file_list[i]   # 获得文件的名字
        class_number = int(file_name_str.split('_')[0])     # 获得分类的数字
        vector_under_test = img2vector('./data/kNN_hand_writing/testDigits/%s' % (file_name_str))   # 获得测试集的 1x1024 向量
        classifier_result = classify0(vector_under_test, training_mat, hw_labels, 6)    # 获得预测结果
        print("分类预测结果：%d\t真实结果：%d"%(classifier_result, class_number))
        if(classifier_result != class_number):
            error_count += 1.0
    print("测试数据总数：%d\t出错数：%d\t错误率：%f%%" % (m_test, error_count, error_count/m_test))

if __name__ == '__main__':
    kNN_hand_written_test()