import math
import random

def load_data():
    data = []
    f = open("/Users/WRL/Desktop/iris.txt", "r")
    for line in f:
        line = line.strip('\n')
        l = line.split(',')
        l[0] = float(l[0])
        l[1] = float(l[1])
        l[2] = float(l[2])
        l[3] = float(l[3])
        data.append(l)
    f.close()
    return data


def cal_eti(raw_data, a_index, a_type):
    data = []
    threshold = [5.95, 3.15, 4.45, 1.45]
    if a_type == "small":
        for i in raw_data:
            if i[a_index] < threshold[a_index]:
                data.append(i)
    else:
        for i in raw_data:
            if i[a_index] > threshold[a_index]:
                data.append(i)

    if len(data) == 0:
        return [0, 0]
    class_cnt0 = 0
    class_cnt1 = 0
    class_cnt2 = 0
    classs = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]

    for i in data:
        if i[4] == classs[0]:
            class_cnt0 += 1
        elif i[4] == classs[1]:
            class_cnt1 += 1
        else:
            class_cnt2 += 1

    prob0 = class_cnt0 / len(data)
    prob1 = class_cnt1 / len(data)
    prob2 = class_cnt2 / len(data)

    if prob0 == 0:
        re0 = 0
    else:
        re0 = prob0 * math.log(prob0, 2)

    if prob1 == 0:
        re1 = 0
    else:
        re1 = prob1 * math.log(prob1, 2)

    if prob2 == 0:
        re2 = 0
    else:
        re2 = prob2 * math.log(prob2, 2)

    re = -(re0 + re1 + re2)
    return [re, len(data)]


def cal_et(data, a_index):
    re_small = cal_eti(data, a_index, "small")
    re_big = cal_eti(data, a_index, "big")
    all_cnt = len(data)
    re = ((re_small[1])/all_cnt)*(re_small[0]) + ((re_big[1])/all_cnt) * (re_big[0])
    return re


#a_list can not be 0
def cal_minet(data, a_index_list):
    min_value = 0
    min_a_index = 0
    min = [min_a_index, min_value]

    nothing = True
    for a_index in a_index_list:
        value = cal_et(data, a_index)
        if nothing:
            min[0] = a_index
            min[1] = value
            nothing = False
        else:
            if value < min[1]:
                min[1] = value
                min[0] = a_index
    return min[0]


class TreeNode:
    def __init__(self, isleaf):
        self.leaf = isleaf
        self.attr_index = None
        self.class_name = None
        self.right = None
        self.left = None

    def set_attr_index(self, index):
        self.attr_index = index

    def set_class_name(self, name):
        self.class_name = name

    def insert_left(self, node):
        self.left = node

    def insert_right(self, node):
        self.right = node


def create_tree_node(data, a_index_list, upper_most_class_index):
    classs = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
    if len(data) == 0:
        # do not have data
        node = TreeNode(True)
        node.set_class_name(classs[upper_most_class_index])
        return node
    elif len(a_index_list) == 0:
        cnt = [0, 0, 0]
        for i in data:
            if i[4] == classs[0]:
                cnt[0] += 1
            elif i[4] == classs[1]:
                cnt[1] += 1
            elif i[4] == classs[2]:
                cnt[2] += 1
            else:
                cnt[3] += 1
        node = TreeNode(True)
        node.set_class_name(classs[cnt.index(max(cnt))])
        return node
    else:
        cnt = [0, 0, 0]
        for i in data:
            if i[4] == classs[0]:
                cnt[0] += 1
            elif i[4] == classs[1]:
                cnt[1] += 1
            elif i[4] == classs[2]:
                cnt[2] += 1
            else:
                cnt[3] += 1
        if max(cnt) == len(data):
            node = TreeNode(True)
            node.set_class_name(classs[cnt.index(max(cnt))])
            return node
        else:
            a_index = cal_minet(data, a_index_list)
            node = TreeNode(False)
            node.set_attr_index(a_index)
            #print(str(a_index_list) + " " + str(a_index))###
            a_index_list.remove(a_index)
            data_small = []
            data_big = []
            threshold = [5.95, 3.15, 4.45, 1.45]
            for i in data:
                if i[a_index] < threshold[a_index]:
                    data_small.append(i)
                else:
                    data_big.append(i)
            small_node = create_tree_node(data_small, a_index_list, cnt.index(max(cnt)))
            big_node = create_tree_node(data_big, a_index_list, cnt.index(max(cnt)))
            node.insert_left(small_node)
            node.insert_right(big_node)
            return node


def _judge(node, item):
    threshold = [5.95, 3.15, 4.45, 1.45]
    pre = ["unknown"]
    while True:
        if node.leaf:
            pre[0] = node.class_name
            break
        else:
            if item[node.attr_index] < threshold[node.attr_index]:
                node = node.left
            else:
                node = node.right
    pre = pre[0]
    return pre


def judge(node_list, item):
    pre = []
    for i in range(len(node_list)):
        pre.append(_judge(node_list[i], item))
    final_pre = max(pre, key=pre.count)
    real = item[4]
    # print(pre + "  " + real)
    if final_pre == real:
        return True
    else:
        return False

def judge_all(node_list, data):
    right = 0
    wrong = 0
    for i in data:
        if judge(node_list, i):
            right += 1
        else:
            wrong += 1
    return right / (right + wrong)


def bagging(raw_data):
    data = []
    for i in range(len(raw_data)):
        data.append(raw_data[round(random.uniform(0, len(raw_data)-1))])
    return data


def ramdom_attr():
    a1 = round(random.uniform(0, 3))
    a2 = round(random.uniform(0, 3))
    return [a1, a2]


if __name__ == "__main__":
    all_data = load_data()

    tree_num = 1
    a = 130
    train_data = all_data[0: a]
    test_data = all_data[a: 150]

    tree_list = []
    for i in range(tree_num):
        tree = create_tree_node(bagging(train_data), ramdom_attr(), 0)
        tree_list.append(tree)

    res = judge_all(tree_list, test_data)
    print("right/(right+wrong = " + str(res))

    print("hello world")
