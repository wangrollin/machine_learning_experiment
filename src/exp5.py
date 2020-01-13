import math
import random

def load_data():
    data = []
    f = open("/Users/WRL/Desktop/wine.txt", "r")
    for line in f:
        line = line.strip('\n')
        l = line.split(',')
        for i in range(14):
            l[i] = float(l[i])
        data.append(l)
    f.close()
    return data


def cal_center(m_data, ksize):
    centers = []
    for i in range(ksize):
        centers.append([])
        for j in range(13):
            centers[i].append(0)
    for i in range(ksize):
        for item in m_data[i]:
            for j in range(13):
                centers[i][j] += item[j+1]
        for j in range(13):
            centers[i][j] /= len(m_data[i])
    return centers


def classify_one(item, centers):
    nothing = True
    min_dis = 0
    min_class = [0]
    for i in range(len(centers)):
        dis = 0
        for j in range(13):
            dis += (centers[i][j]-item[j+1])**2
        dis = math.sqrt(dis)

        if nothing:
            min_dis = dis
            min_class[0] = i
            nothing = False
        else:
            if dis < min_dis:
                min_dis = dis
                min_class[0] = i
            # guess     real
    return [min_class[0], item[0]]


def cal_new_class(indata, centers):
    data = []
    for i in range(len(centers)):
        data.append([])
    for item in indata:
        data[classify_one(item, centers)[0]].append(item)
    return data


def iter_classify(data, ksize):
    for i in range(len(data) - 1):
        for j in range(13):
            data[len(data) - 1][j + 1] += data[i][j + 1]
    for j in range(13):
        data[len(data) - 1][j + 1] /= len(data)
    avg = (data[len(data) - 1])[1: 14]

    centers = []
    for i in range(ksize):
        centers.append([])
        for j in range(13):
            centers[i].append(avg[j]*random.uniform(0.8, 1.2))

    for i in range(60):
        m_data = cal_new_class(data, centers)
        centers = cal_center(m_data, ksize)

    for class_index in range(len(m_data)):
        l = []
        for item in m_data[class_index]:
            l.append(item[0])
        print(l)


if __name__ == "__main__":
    ksize = 5
    print("ksize = " + str(ksize))
    iter_classify(load_data(), ksize)
    print("hello world")
