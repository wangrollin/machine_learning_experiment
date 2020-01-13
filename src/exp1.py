# load all the data
def load():
    f = open("/Users/WRL/Desktop/exp1.txt", "r")
    re = list()
    for line in f:
        line = line.strip('\n')
        a = line.split(",")
        re.append(a)
    f.close()
    return re


# calculate the probability of each class P(Yi)
def get_pyi(data):
    count = [0, 0, 0, 0]
    for i in data:
        if i[6] == "unacc":
            count[0] += 1
        elif i[6] == "acc":
            count[1] += 1
        elif i[6] == "good":
            count[2] += 1
        else:
            count[3] += 1
    data_size = len(data)
    pyi = [count[0]/data_size, count[1]/data_size, count[2]/data_size, count[3]/data_size]
    return pyi


def cal_a0(data):
    yiai = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    classs = ["unacc", "acc", "good", "vgood"]
    buying = ["vhigh", "high", "med", "low"]
    for i in data:
        yiai[classs.index(i[6])][buying.index(i[0])] += 1

    num = [1210, 384, 69, 65]
    for i in range(4):
        for j in range(4):
            yiai[i][j] /= num[i]

    return yiai


def cal_a1(data):
    yiai = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    classs = ["unacc", "acc", "good", "vgood"]
    maint = ["vhigh", "high", "med", "low"]
    for i in data:
        yiai[classs.index(i[6])][maint.index(i[1])] += 1

    num = [1210, 384, 69, 65]
    for i in range(4):
        for j in range(4):
            yiai[i][j] /= num[i]

    return yiai


def cal_a2(data):
    yiai = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    classs = ["unacc", "acc", "good", "vgood"]
    door = ["2", "3", "4", "5more"]
    for i in data:
        yiai[classs.index(i[6])][door.index(i[2])] += 1

    num = [1210, 384, 69, 65]
    for i in range(4):
        for j in range(4):
            yiai[i][j] /= num[i]

    return yiai


def cal_a3(data):
    yiai = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    classs = ["unacc", "acc", "good", "vgood"]
    persons = ["2", "4", "more"]
    for i in data:
        yiai[classs.index(i[6])][persons.index(i[3])] += 1

    num = [1210, 384, 69, 65]
    for i in range(4):
        for j in range(3):
            yiai[i][j] /= num[i]

    return yiai


def cal_a4(data):
    yiai = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    classs = ["unacc", "acc", "good", "vgood"]
    lug_boot = ["small", "med", "big"]
    for i in data:
        yiai[classs.index(i[6])][lug_boot.index(i[4])] += 1

    num = [1210, 384, 69, 65]
    for i in range(4):
        for j in range(3):
            yiai[i][j] /= num[i]

    return yiai


def cal_a5(data):
    yiai = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
    classs = ["unacc", "acc", "good", "vgood"]
    safety = ["low", "med", "high"]
    for i in data:
        yiai[classs.index(i[6])][safety.index(i[5])] += 1

    num = [1210, 384, 69, 65]
    for i in range(4):
        for j in range(3):
            yiai[i][j] /= num[i]

    return yiai


# count all the yi_ai
def get_allp(data):
    allp = [cal_a0(data), cal_a1(data), cal_a2(data),
            cal_a3(data), cal_a4(data), cal_a5(data)]
    return allp


# classify
def classify_one(item, pyi, allp):
    classs = ["unacc", "acc", "good", "vgood"]
    buying = ["vhigh", "high", "med", "low"]
    maint = ["vhigh", "high", "med", "low"]
    door = ["2", "3", "4", "5more"]
    persons = ["2", "4", "more"]
    lug_boot = ["small", "med", "big"]
    safety = ["low", "med", "high"]
    attr = [buying, maint, door, persons, lug_boot, safety]

    p0 = pyi[0]
    p1 = pyi[1]
    p2 = pyi[2]
    p3 = pyi[3]
    for attr_index in range(6):
        p0 *= allp[attr_index][0][attr[attr_index].index(item[attr_index])]
        p1 *= allp[attr_index][1][attr[attr_index].index(item[attr_index])]
        p2 *= allp[attr_index][2][attr[attr_index].index(item[attr_index])]
        p3 *= allp[attr_index][3][attr[attr_index].index(item[attr_index])]

    re = classs[0]
    if max(p0, p1, p2, p3) == p0:
        re = classs[0]
    elif max(p0, p1, p2, p3) == p1:
        re = classs[1]
    elif max(p0, p1, p2, p3) == p2:
        re = classs[2]
    else:
        re = classs[3]

    if re == item[6]:
        return True
    else:
        return False


def classify(data, pyi, allp):
    right = 0
    wrong = 0
    for i in data:
        if classify_one(i, pyi, allp):
            right += 1
        else:
            wrong += 1
    return right/(right+wrong)


if __name__ == "__main__":
    data = load() #0-1727
    # learn to build
    pre_num = [100, 200, 500, 700, 1000, 1350]
    for i in range(6):
        data1 = data[0: pre_num[i]]
        pyi = get_pyi(data1)
        allp = get_allp(data1)
        # classify
        data2 = data[pre_num[i]: 1728]
        print("train num: " + str(pre_num[i]) + ", right/(right+wrong) = " + str(classify(data2, pyi, allp)))
