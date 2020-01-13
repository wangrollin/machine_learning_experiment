import os
import math


def file_trainlist():
    set = os.listdir("/Users/WRL/Desktop/digits/trainingDigits")
    return set


def file_testlist():
    set = os.listdir("/Users/WRL/Desktop/digits/testDigits")
    return set


def get_content(path):
    f = open(path, "r")
    data = []
    for line in f:
        data.append(line.strip('\n'))
    f.close()
    return data


def cal_distance(num1_data, num2_data):
    dis = 0
    for i in range(32):
        for j in range(32):
            dis += (int(num1_data[i][j]) - int(num2_data[i][j]))**2
    return math.sqrt(dis)


def get_num(full_path):
    first = full_path.rfind('/')
    end = full_path.rfind('.')
    re = full_path[first+1: end]
    return re


def remove_max(knn):
    values = list(knn.values())
    values.sort(reverse=True)
    maxv = values[0]
    for k, v in knn.items():
        if v == maxv:
            knn.pop(k)
            break
    return


def get_max(knn):
    value = list(knn.values())
    value.sort(reverse=True)
    maxv = value[0]
    return maxv


def cal_predict(ksize, num_data, trainset):
    knn = {}
    for train_data in trainset:
        dis = cal_distance(num_data, get_content(train_data))
        if len(knn) < ksize:
            knn.update({get_num(train_data): dis})
        elif dis < get_max(knn):
            remove_max(knn)
            knn.update({get_num(train_data): dis})
    knn_num = {}
    for k, v in knn.items():
        num = k[0: k.index('_')]
        if num in knn_num.keys():
            knn_num.update({num: knn_num.get(num) + 1})
        else:
            knn_num.update({num: 1})
    l = list(knn_num.values())
    l.sort(reverse=True)
    maxcount = l[0]
    for k, v in knn_num.items():
        if v == maxcount:
            #print(k)
            return k


def judge(ksize, testpath, trainset):
    num_data = get_content(testpath)
    guess = cal_predict(ksize, num_data, trainset)
    real = get_num(testpath)
    real = real[0: real.index('_')]
    #print("guess:"+int(guess))
    #print("real"+int(real)+"\n\n")
    if real == guess:
        return True
    else:
        return False


def testall(ksize):
    testset = file_testlist()
    trainset = file_trainlist()

    for i in range(len(testset)):
        testset[i] = "/Users/WRL/Desktop/digits/testDigits/" + testset[i]
    for i in range(len(trainset)):
        trainset[i] = "/Users/WRL/Desktop/digits/trainingDigits/" + trainset[i]

    right = 0
    wrong = 0
    for test_path in testset:
        if judge(ksize, test_path, trainset):
            print("Yes")
            right += 1
        else:
            print("No")
            wrong += 1
    return right / (right + wrong)


if __name__ == "__main__":
    ksize = 3
    a = testall(ksize)
    print(a)
    print("hello world")
