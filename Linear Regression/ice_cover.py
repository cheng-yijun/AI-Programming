import math
import csv
import random


def get_dataset():
    mydata = []
    f = csv.reader(open('mydataset.csv'))
    for i in f:
        tmp = [int(i[0]), int(i[1])]
        mydata.append(tmp)
    return mydata


def print_stats(dataset):
    print(len(dataset))
    sum = 0
    for i in dataset:
        sum = sum + i[1]
    avg = sum / len(dataset)
    print("{:.2f}".format(round(avg, 2)))
    sd_dum = 0
    for i in dataset:
        sd_dum = sd_dum + (i[1] - avg) ** 2
    sd_dum = sd_dum / (len(dataset) - 1)
    sd_dum = math.sqrt(sd_dum)
    print("{:.2f}".format(round(sd_dum, 2)))


def regression(beta_0, beta_1, dataset=None):
    if dataset is None:
        dataset = get_dataset()
    sum = 0
    for i in dataset:
        sum = sum + (beta_0 + beta_1 * i[0] - i[1]) ** 2
    mse = sum / len(dataset)
    return mse


def gradient_descent(beta_0, beta_1, dataset=None):
    if dataset is None:
        dataset = get_dataset()
    sum = 0
    for i in dataset:
        sum = sum + beta_0 + beta_1 * i[0] - i[1]
    mse0 = (2 * sum) / len(dataset)
    sum = 0
    for i in dataset:
        sum = sum + (beta_0 + beta_1 * i[0] - i[1]) * i[0]
    mse1 = (2 * sum) / len(dataset)
    tup = (mse0, mse1)
    return tup


def iterate_gradient(T, eta):
    beta0 = [0]
    beta1 = [0]
    for i in range(1, T + 1):
        tmp0 = beta0[i - 1] - eta * gradient_descent(beta0[i - 1], beta1[i - 1])[0]
        beta0.append(tmp0)
        tmp1 = beta1[i - 1] - eta * gradient_descent(beta0[i - 1], beta1[i - 1])[1]
        beta1.append(tmp1)
        print(str(i) + ' ' + str("{:.2f}".format(round(tmp0, 2))) + ' ' + str("{:.2f}".format(round(tmp1, 2))) + ' ' + str(
            "{:.2f}".format(round(regression(tmp0, tmp1), 2))))


def compute_betas():
    dataset = get_dataset()
    sumx = sumy = 0
    for i in dataset:
        sumx = sumx + i[0]
        sumy = sumy + i[1]
    avgx = sumx / len(dataset)
    avgy = sumy / len(dataset)
    sum_high = 0
    sum_low = 0
    for i in dataset:
        sum_high = sum_high + ((i[0] - avgx) * (i[1] - avgy))
        sum_low = sum_low + (i[0] - avgx) ** 2
    beta1 = sum_high / sum_low
    beta0 = avgy - beta1 * avgx
    mse = regression(beta0, beta1)
    tup = (beta0, beta1, mse)
    return tup


def predict(year):
    tup = compute_betas()
    beta0 = tup[0]
    beta1 = tup[1]
    days = beta0 + beta1 * year
    return days


def iterate_normalized(T, eta):
    sum = 0
    dataset = get_dataset()
    for i in dataset:
        sum = sum + i[0]
    avgx = sum / len(dataset)
    sum = 0
    for i in dataset:
        sum = sum + (i[0] - avgx) ** 2
    stdx = math.sqrt(sum / (len(dataset) - 1))
    new_dataset = []
    for i in dataset:
        tmp = [(i[0] - avgx) / stdx, i[1]]
        new_dataset.append(tmp)
    beta0 = [0]
    beta1 = [0]
    for i in range(1, T + 1):
        tmp0 = beta0[i - 1] - eta * gradient_descent(beta0[i - 1], beta1[i - 1], new_dataset)[0]
        beta0.append(tmp0)
        tmp1 = beta1[i - 1] - eta * gradient_descent(beta0[i - 1], beta1[i - 1], new_dataset)[1]
        beta1.append(tmp1)
        print(str(i) + ' ' + str("{:.2f}".format(round(tmp0, 2))) + ' ' + str("{:.2f}".format(round(tmp1, 2))) + ' ' + str(
            "{:.2f}".format(round(regression(tmp0, tmp1, new_dataset), 2))))


def sgd(T, eta):
    dataset = get_dataset()
    beta0 = [0]
    beta1 = [0]
    sum = 0
    for i in dataset:
        sum = sum + i[0]
    avgx = sum / len(dataset)
    sum = 0
    for i in dataset:
        sum = sum + (i[0] - avgx) ** 2
    stdx = math.sqrt(sum / (len(dataset) - 1))
    new_dataset = []
    for i in dataset:
        tmp = [(i[0] - avgx) / stdx, i[1]]
        new_dataset.append(tmp)
    for i in range(1, T + 1):
        pick = random.choice(range(1, len(dataset) - 1))
        tmp0 = beta0[i - 1] - eta * 2 * (beta0[i - 1] + beta1[i - 1] * new_dataset[pick][0] - new_dataset[pick][1])
        beta0.append(tmp0)
        tmp1 = beta1[i - 1] - eta * 2 * (beta0[i - 1] + beta1[i - 1] * new_dataset[pick][0] - new_dataset[pick][1]) * \
               new_dataset[pick][0]
        beta1.append(tmp1)
        print(str(i) + ' ' + str("{:.2f}".format(round(tmp0, 2))) + ' ' + str("{:.2f}".format(round(tmp1, 2))) + ' ' + str(
            "{:.2f}".format(round(regression(tmp0, tmp1, new_dataset), 2))))

