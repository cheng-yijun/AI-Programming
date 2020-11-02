import os
import numpy as np


#  Get all files in the given directory
def getAllFiles(directory):
    File_list = os.listdir(directory)
    allFiles = list()
    for entry in File_list:
        # create a path
        path = os.path.join(directory, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(path):
            allFiles = allFiles + getAllFiles(path)
        else:
            allFiles.append(path)
    return allFiles


#  create and return a vocabulary as a list of word types
#  with counts >= cutoff in the training directory
def create_vocabulary(training_directory, cutoff):
    allFiles = getAllFiles(training_directory)
    dict = {}
    for filename in allFiles:
        try:
            f = open(filename, 'r')
            lines = f.readlines()
            for token in lines:  # one line one token
                token = token.strip()
                if token not in dict.keys():
                    dict[token] = 1
                else:
                    dict[token] += 1
        except:
            continue
    vocab = []
    for v in dict.keys():
        if dict[v] >= cutoff:
            vocab.append(v)
    vocab.sort()
    return vocab


#   create and return a bag of words Python dictionary from a single document
def create_bow(vocab, filepath):
    dict = {}
    try:
        f = open(filepath, 'r')
        lines = f.readlines()
        for token in lines:  # one line one token
            token = token.strip()
            if token in vocab:  # find the token in vocab
                if token in dict.keys():
                    dict[token] += 1
                else:
                    dict[token] = 1
            else:  # token is not in vocab
                if None in dict.keys():
                    dict[None] += 1
                else:
                    dict[None] = 1
        f.close()
    except:
        return None
    return dict


#  create and return training set (bag of words Python
#  dictionary + label) from the files in a training directory
def load_training_data(vocab, directory):
    data_set = []
    File_list = os.listdir(directory)
    File_list.sort()
    for entry in File_list:
        path = os.path.join(directory, entry)
        if os.path.isdir(path):
            files = os.listdir(path)
            for filename in files:
                dict = {'label': entry}
                filepath = os.path.join(path, filename)
                dict['bow'] = create_bow(vocab, filepath)
                if dict['bow'] is not None:
                    data_set.append(dict)
    return data_set


#  given a training set, estimate and return
#  the prior probability p(label) of each label
def prior(training_data, label_list):
    log_prob = {}
    for label in label_list:
        count = 0
        for dict in training_data:
            if dict['label'] == label:
                count += 1
        log_prob[label] = np.log(count) - np.log(len(training_data))
    return log_prob


#  count the total frequency of label in the given training data set
def count_total(training_data, label):
    total = 0
    for dict in training_data:
        if dict['label'] == label:
            for key in dict['bow'].keys():
                total = total + dict['bow'][key]
    return total


#  given a training set and a vocabulary, estimate and return the
#  class conditional distribution: P(word|abel) over all words for the given label using smoothing
def p_word_given_label(vocab, training_data, label):
    word_prob_log = {}
    total = count_total(training_data, label) + len(vocab)
    for v in vocab:
        count = 0
        for dict in training_data:
            if dict['label'] == label and v in dict['bow'].keys():
                count = count + dict['bow'][v]
        word_prob_log[v] = np.log(count + 1) - np.log(total + 1)
    # compute for None
    count_None = 0
    for dict in training_data:
        if dict['label'] == label and None in dict['bow'].keys():
            count_None = count_None + dict['bow'][None]
    word_prob_log[None] = np.log(count_None + 1) - np.log(total + 1)
    return word_prob_log


#  loads the training data, estimates the prior distribution
#  P(label) and class conditional distributions P(word|abel)，
#  return the trained model
def train(training_directory, cutoff):
    model = {}
    # get all labels
    File_list = os.listdir(training_directory)
    File_list.sort()
    labels = []
    for entry in File_list:
        path = os.path.join(training_directory, entry)
        if os.path.isdir(path):
            labels.append(entry)

    # training
    vocab = create_vocabulary(training_directory, cutoff)
    model['vocabulary'] = vocab
    training_data = load_training_data(vocab, training_directory)
    log_prior = prior(training_data, labels)
    model['log prior'] = log_prior
    for label in labels:
        key = 'log p(w|y=' + label + ')'
        model[key] = p_word_given_label(vocab, training_data, label)
    return model


#  given a trained model, predict the label for the test document
#  (see below for implementation details including return value)
def classify(model, filepath):
    max_log = float("-inf")
    pre_class = None
    classify_result = {}
    # get the vocabulary
    vocab = {}
    f = open(filepath, 'r')
    lines = f.readlines()
    for token in lines:
        token = token.strip()
        if token not in vocab.keys():
            vocab[token] = 1
        else:
            vocab[token] += 1
    for key in model['log prior']:
        prediction = 0
        log_p = 'log p(w|y=' + key + ')'
        for word in vocab.keys():
            if word in model[log_p].keys():
                prediction = prediction + vocab[word] * model[log_p][word]
            else:
                prediction = prediction + vocab[word] * model[log_p][None]
        prediction = prediction + model['log prior'][key]
        arg = 'log p(y=' + key + '|x)'
        classify_result[arg] = prediction
        if prediction > max_log:
            max_log = prediction
            pre_class = key
    classify_result['predicted y'] = pre_class
    return classify_result

def classify_all(model, dire):
    y = 0
    count = 0
    files = getAllFiles(dire)
    for file in files:
        if '.DS_Store' in file:
            continue
        c = classify(model, file)
        count += 1
        if c['predicted y'] == '2020':
            y += 1
    print(y / count)

# def test_neutral():
#     count = 0
#     count_neu = 0
#     model = train('./sentiment_analysis/train/', 35)
#     for i in range(1000):
#         filepath = 'sentiment_analysis/test/neutral/' + str(count_neu) + '.txt'
#         result = classify(model, filepath)
#         count_neu += 1
#         if result['predicted y'] == 'neutral':
#             count += 1
#     accuracy = count / 1000
#     return accuracy
#
# def test_pos():
#     count = 0
#     count_pos = 0
#     model = train('./sentiment_analysis/train/', 35)
#     for i in range(1000):
#         filepath = 'sentiment_analysis/test/positive/' + str(count_pos) + '.txt'
#         result = classify(model, filepath)
#         count_pos += 1
#         if result['predicted y'] == 'positive':
#             count += 1
#     accuracy = count / 1000
#     return accuracy
#
# def test_neg():
#     count = 0
#     count_neg = 0
#     model = train('./sentiment_analysis/train/', 35)
#     for i in range(1000):
#         filepath = 'sentiment_analysis/test/negative/' + str(count_neg) + '.txt'
#         result = classify(model, filepath)
#         count_neg += 1
#         if result['predicted y'] == 'negative':
#             count += 1
#     accuracy = count / 1000
#     return accuracy
#
# print(train('./sentiment_analysis/train/', 2))

# print('neutral: ' + str(test_neutral()))
# print('positive: ' + str(test_pos()))
# print('negative: ' + str(test_neg()))
#print(create_vocabulary('./sentiment_analysis/train', 35))
# model = train('./sentiment_analysis/train/', 35)
# print(classify(model, './test_file.txt'))
# model = train('./corpus/training/', 3)
# # classify_all(model, './corpus/test/2020')
# print(classify(model, './EasyFiles/2016/1.txt'))