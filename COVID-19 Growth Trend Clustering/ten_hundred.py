import csv
import math


def load_data(filepath):
    data_dicts = []
    f = csv.reader(open(filepath))
    for i in f:
        row_dict = {'Province/State': i[0], 'Country/Region': i[1]}
        i = i[4:]
        row_dict['case'] = i
        data_dicts.append(row_dict)
    data_dicts = data_dicts[1:]
    return data_dicts


def calculate_x_y(time_series):
    time_list = time_series['case']
    index_x = 0
    index_y = 0
    find_x = False
    find_y = False

    if time_list[len(time_list) - 1] == '0':
        x = float('NaN')
        y = float('NaN')
        tup = (x, y)
        return tup

    for i in reversed(range(len(time_list))):
        if float(time_list[i]) <= int(time_list[len(time_list) - 1]) / 10:
            index_x = i
            find_x = True
            break
    for i in reversed(range(len(time_list))):
        if float(time_list[i]) <= int(time_list[len(time_list) - 1]) / 100:
            index_y = i
            find_y = True
            break
    if find_x is False:
        x = float('NaN')
    else:
        x = len(time_list) - 1 - index_x
    if find_y is False:
        y = float('NaN')
    else:
        y = index_x - index_y
    tup = (x, y)
    return tup


def hac(dataset):  # input exp: Afghanistan [(13, 25),(20, 23), (14, 29)]
    tmp_dataset = []
    for element in dataset:
        if not math.isnan(element[0]) and not math.isnan(element[1]):
            tmp_dataset.append(element)
    dataset = tmp_dataset

    outer_cluster = []  # initial: 0 ... 244
    for num in range(len(dataset)):
        outer_cluster.append([num])

    min_dis = []  # the list contain all pair points with computed shortest distance
    Z = []
    if_skip = False
    tmp_min = float('inf')  # min distance record variable
    min_tup = ()
    for k in range(len(dataset) - 1):  # loop to clustering
        for i in range(len(dataset)):  # loop to compare distance
            for j in range(i + 1, len(dataset)):
                for md in min_dis:  # check if these two points have been added
                    if i in md and j in md:  # case: have been computed
                        if_skip = True
                        break
                for kk in range(len(outer_cluster)):
                    index = len(outer_cluster) - kk - 1
                    if len(outer_cluster[index]) == 1:  # these two points cannot in one cluster
                        break
                    if i in outer_cluster[index] and j in outer_cluster[index]:
                        if_skip = True
                        break
                if if_skip:
                    if_skip = False
                    continue  # compute distance of next pair of points
                # this pair have not been computed yet
                # compute distance between these two points
                cur_dis = math.sqrt(sum([(a - b) ** 2 for a, b in zip(dataset[i], dataset[j])]))
                if cur_dis < tmp_min:  # find shorter distance pair
                    tmp_min = cur_dis
                    min_tup = (i, j)
                if cur_dis == tmp_min:
                    cur_i = -1
                    cur_j = -1
                    recorded_i = -1
                    recorded_j = -1
                    for index1 in reversed(range(len(outer_cluster))):
                        if i in outer_cluster[index1]:
                            cur_i = index1
                            break
                    for index1 in reversed(range(len(outer_cluster))):
                        if j in outer_cluster[index1]:
                            cur_j = index1
                            break
                    for index1 in reversed(range(len(outer_cluster))):
                        if min_tup[0] in outer_cluster[index1]:
                            recorded_i = index1
                            break
                    for index1 in reversed(range(len(outer_cluster))):
                        if min_tup[1] in outer_cluster[index1]:
                            recorded_j = index1
                            break
                    aa = min(cur_i, cur_j)
                    bb = min(recorded_i, recorded_j)
                    cc = max(cur_i, cur_j)
                    dd = max(recorded_i, recorded_j)
                    if aa < bb or aa == bb and cc < dd:
                        min_tup = (i, j)
        # has found the shortest pair in this round
        min_dis.append(min_tup)
        cluster_num_i = -1
        # print(len(outer_cluster))
        for kk in range(len(outer_cluster)):
            index1 = len(outer_cluster) - kk - 1
            # print(str(i) + ' ' + str(kk) + ' ' + str(index1) + ' ' + str(outer_cluster[index1]))
            if min_tup[0] in outer_cluster[index1]:
                cluster_num_i = index1
                break
        cluster_num_j = -1
        for kk in range(len(outer_cluster)):
            index2 = len(outer_cluster) - kk - 1
            if min_tup[1] in outer_cluster[index2]:
                cluster_num_j = index2
                break
        num_points = len(outer_cluster[cluster_num_i]) + len(outer_cluster[cluster_num_j])
        entrance = [min(cluster_num_i, cluster_num_j), max(cluster_num_i, cluster_num_j), tmp_min, num_points]
        Z.append(entrance)
        new_points_set = outer_cluster[cluster_num_i] + outer_cluster[cluster_num_j]
        outer_cluster.append(new_points_set)

        # re-initialize for next loop
        tmp_min = float('inf')
        if_skip = False
    return Z


# data = load_data('time_series_covid19_confirmed_global.csv')
#
# X = []
# for i in data:
#     dis = calculate_x_y(i)
#     # if not math.isnan(dis[0]) and not math.isnan(dis[1]):
#     X.append(dis)
#
# Z = hac(X)
# for z in Z:
#     print(z)
