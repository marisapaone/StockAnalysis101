# -*- coding: utf-8 -*-
"""
@author: Marisa Paone
Class: CS677
Facilitator: Sarah Cameron
Date: 7/17/23
Homework#2 Problems 1-5

this scripts reads ticker files (e.g. PG.csv and SPY.csv) and performs data science operations on them.
It also creates line plots! Uses pandas, numpy and matplotlib.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Importing and reading two .csv files into pandas dataframes

ticker='PG'
here = os.path.abspath(__file__)
input_dir = os.path.abspath(os.path.join(here, os.pardir))
df = pd.read_csv(os.path.join(input_dir, ticker + '.csv'))


ticker2='SPY'
here2 = os.path.abspath(__file__)
input_dir2 = os.path.abspath(os.path.join(here, os.pardir))
df2 = pd.read_csv(os.path.join(input_dir2, ticker2 + '.csv'))

try:
    # Adding a true label column to each dataframe object based on + or - returns.
    # dataframe df is for my ticker PG, and dataframe df2 is for ticker SPY.

    df["True_Label"] = np.where(df['Return'] >= 0, '+', '-')

    df2["True_Label"] = np.where(df2['Return'] >= 0, '+', '-')

    print()
    print("------------Question 1 Part 1------------")
    print()
    print("Table data for ticker:", ticker)
    print(df)

    print("Table data for ticker:", ticker2)
    print(df2)

    print()
    print("------------Question 1 Part 2------------")
    print()

    # Creating the training set for PG from years 2016, 2017 and 2018
    print("Training Set for PG")
    grouped = df.groupby(df.Year)
    train_set_2016 = grouped.get_group(2016)
    train_set_2017 = grouped.get_group(2017)
    train_set_2018 = grouped.get_group(2018)

    train_set = train_set_2016._append(train_set_2017)
    train_set = train_set._append(train_set_2018)

    # Counting the positive and negative labels of the train set for PG.
    pos_count = len(train_set[train_set["True_Label"] == '+'])
    print('The positive return day count of the PG training set is', pos_count)
    neg_count = len(train_set[train_set["True_Label"] == '-'])
    print('The negative return day count of the PG training set is', neg_count)
    print('Probability of an up day for PG:', round((pos_count/(pos_count+neg_count))*100, 2), '%')
    print('Probability of a down day got PG:', round((neg_count/(pos_count+neg_count))*100, 2), '%')
    print()

    # Creating the training set for SPY from years 2016, 2017 and 2018
    print("Training Set for SPY")
    grouped2 = df2.groupby(df2.Year)
    train_set_2016_SP = grouped2.get_group(2016)
    train_set_2017_SP = grouped2.get_group(2017)
    train_set_2018_SP = grouped2.get_group(2018)

    train_set_SP = train_set_2016_SP._append(train_set_2017_SP)
    train_set_SP = train_set_SP._append(train_set_2018_SP)

    # Counting the positive and negative labels of the train set for SPY.
    pos_count_SP = len(train_set_SP[train_set_SP["True_Label"] == '+'])
    print('The positive return day count of the SPY training set is', pos_count_SP)
    neg_count_SP = len(train_set_SP[train_set_SP["True_Label"] == '-'])
    print('The negative return day count of the SPY training set is', neg_count_SP)
    print('Probability of an up day for SPY:', round((pos_count_SP / (pos_count_SP + neg_count_SP)) * 100, 2), '%')
    print('Probability of a down day for SPY:', round((neg_count_SP / (pos_count_SP + neg_count_SP)) * 100, 2), '%')

    print()
    print("-----------Question 1 Part 3-----------")
    print()
    # Part 3 Consecutive down days
    # Adding a row of 0's and 1's... for the -'s it will populate with 0's and for the +'s they will be 1's
    train_set['Zeros_or_Ones'] = np.where(train_set['True_Label'] == '-', 0, 1)
    # Adds a row counter, to calculate the cumulative sum of these 0's and 1's
    train_set['counter'] = train_set['Zeros_or_Ones'].ne(0).cumsum()

    train_set_SP['Zeros_or_Ones'] = np.where(train_set_SP['True_Label'] == '-', 0, 1)
    train_set_SP['counter'] = train_set_SP['Zeros_or_Ones'].ne(0).cumsum()

    # if the counter increments by 1 then you have two up days in a row.

    # Appends to new_set list where the last consecutive negative is (but the next i is A POSITIVE val)
    # Iterates through the counter column, and if the counter value equals the value moved up k spots (meaning its been all zeros/negatives,
    # and the next counter value is less than the next counter value moved up k spots, then add that value to new_set.
    # This means -, -, ... then a + appears (e.g. if k = 2, then its -, -, +)
    # Inside this new_set, is the location of where the last consecutive down was (i+k).
    def consec_down_then_up(k,set):
        new_set = []
        for i in set.index:
            # for the last sequence
            if i == len(set['counter'])-k:
                break #break because theres nothing after this
            if set['counter'][i] == set['counter'][i+k]:
                if set['counter'][i+1] < set['counter'][i+k+1]:
                    new_set.append(i+k)
        return new_set

    # Adds the index i+k where the last consecutive negative is (but the next i is ANOTHER negative val)
    def consec_down_then_down(k,set):
        new_set = []
        for i in set.index:
            # for the last sequence
            if i == len(set['counter'])-k:
                break
            if set['counter'][i] == set['counter'][i+k]:
                if set['counter'][i+1] == set['counter'][i+k+1]:
                    new_set.append(i+k)
        return new_set

    # Calculating the probabilities after seen a certain amount of DOWN days...
    print('FOR TICKER PG:')
    print('The probability after seeing 3 consecutive DOWN days with the next day as an UP day is:',
          (len(consec_down_then_up(3,train_set))/(len(consec_down_then_up(3,train_set))+len(consec_down_then_down(3,train_set))))* 100, '%')
    print('The probability after seeing 3 consecutive DOWN days with the next day as a DOWN day is:',
          (len(consec_down_then_down(3,train_set))/(len(consec_down_then_up(3,train_set))+len(consec_down_then_down(3,train_set))))* 100, '%')

    print()
    print('The probability after seeing 2 consecutive DOWN days with the next day as an UP day is:',
          (len(consec_down_then_up(2,train_set))/(len(consec_down_then_up(2,train_set))+len(consec_down_then_down(2,train_set))))* 100, '%')
    print('The probability after seeing 2 consecutive DOWN days with the next day as a DOWN day is:',
          (len(consec_down_then_down(2,train_set))/(len(consec_down_then_up(2,train_set))+len(consec_down_then_down(2,train_set))))* 100, '%')

    print()
    print('The probability after seeing 1 consecutive DOWN days with the next day as an UP day is:',
          (len(consec_down_then_up(1,train_set))/(len(consec_down_then_up(1,train_set))+len(consec_down_then_down(1,train_set))))* 100, '%')
    print('The probability after seeing 1 consecutive DOWN days with the next day as a DOWN day is:',
          (len(consec_down_then_down(1,train_set))/(len(consec_down_then_up(1,train_set))+len(consec_down_then_down(1,train_set))))* 100, '%')

    print()
    print('FOR TICKER SPY:')
    print('The probability after seeing 3 consecutive DOWN days with the next day as an UP day is:',
          (len(consec_down_then_up(3, train_set_SP)) / (len(consec_down_then_up(3, train_set_SP)) + len(consec_down_then_down(3, train_set_SP)))) * 100, '%')
    print('The probability after seeing 3 consecutive DOWN days with the next day as a DOWN day is:',
          (len(consec_down_then_down(3, train_set_SP)) / (len(consec_down_then_up(3, train_set_SP)) + len(consec_down_then_down(3, train_set_SP)))) * 100, '%')

    print()
    print('The probability after seeing 2 consecutive DOWN days with the next day as an UP day is:',
          (len(consec_down_then_up(2, train_set_SP)) / (len(consec_down_then_up(2, train_set_SP)) + len(consec_down_then_down(2, train_set_SP)))) * 100, '%')
    print('The probability after seeing 2 consecutive DOWN days with the next day as a DOWN day is:',
          (len(consec_down_then_down(2, train_set_SP)) / (len(consec_down_then_up(2, train_set_SP)) + len(consec_down_then_down(2, train_set_SP)))) * 100, '%')

    print()
    print('The probability after seeing 1 consecutive DOWN days with the next day as an UP day is:',
          (len(consec_down_then_up(1, train_set_SP)) / (len(consec_down_then_up(1, train_set_SP)) + len(consec_down_then_down(1, train_set_SP)))) * 100, '%')
    print('The probability after seeing 1 consecutive DOWN days with the next day as a DOWN day is:',
          (len(consec_down_then_down(1, train_set_SP)) / (len(consec_down_then_up(1, train_set_SP)) + len(consec_down_then_down(1, train_set_SP)))) * 100, '%')

    print()
    print("-----------Question 1 Part 4-----------")

    # For every i in the set, if the counter has increased by k, and that value is equal to where it should be (i+k),
    # then test if the counter one past that spot (i+k+1) is greater than the spot before it.
    # If so, then append the index+1 to the new_set. Inside this new_set, is the location of where the last consecutive up was.
    def consec_up_then_up(k, set):
        new_set = []
        for i in set.index:
            # for the last sequence
            if i == len(set['counter']) - k:
                break
            # for the first index
            if i == 0:
                # if the first counter index 0 plus k, is equal to the value of the index i+k (meaning there are k up's)
                if set['counter'][i] + k == set['counter'][i + k]:
                    # And the next one following this is another up, then append this location i+1 (1) to the new_set.
                    if set['counter'][i + k] == set['counter'][i + k + 1]:
                        new_set.append(i + 1)
            # For all other i's
            if set['counter'][i]+k == set['counter'][i + k]:
                if i+k+1 == len(set['counter']):
                    break
                if set['counter'][i + k + 1] > set['counter'][i + k]:
                    new_set.append(i + k)
        return new_set

    # Does the same thing the above function does, but then tests if the last one is a -.
    def consec_up_then_down(k,set):
        new_set = []
        for i in set.index:
            # for the last sequence
            if i == len(set['counter']) - k:
                break
            if i == 0:
                if set['counter'][i] + k - 1 == set['counter'][i + k]:
                    if set['counter'][i + k] == set['counter'][i + k + 1]:
                        new_set.append(i + 1)
            if set['counter'][i] + k == set['counter'][i + k]:
                # for the last value
                if i + k + 1 == len(set['counter']):
                    break
                if set['counter'][i + k] == set['counter'][i + k + 1]:
                    new_set.append(i + k)
        return new_set

    # Calculating the probabilities after seen a certain amount of UP days...

    print()
    print('FOR TICKER PG:')
    print('The probability after seeing 3 consecutive UP days, that the next day is an UP day is',
          (len(consec_up_then_up(3, train_set))/(len(consec_up_then_down(3, train_set))+len(consec_up_then_up(3, train_set))))*100, '%')
    print('The probability after seeing 3 consecutive UP days, that the next day is an DOWN day is',
          (len(consec_up_then_down(3, train_set)) / (len(consec_up_then_down(3, train_set)) + len(consec_up_then_up(3, train_set)))) * 100, '%')

    print()
    print('The probability after seeing 2 consecutive UP days, that the next day is an UP day is',
          (len(consec_up_then_up(2, train_set))/(len(consec_up_then_down(2, train_set))+len(consec_up_then_up(2, train_set))))*100, '%')
    print('The probability after seeing 2 consecutive UP days, that the next day is an DOWN day is',
          (len(consec_up_then_down(2, train_set)) / (len(consec_up_then_down(2, train_set)) + len(consec_up_then_up(2, train_set)))) * 100, '%')

    print()
    print('The probability after seeing 1 consecutive UP days, that the next day is an UP day is',
          (len(consec_up_then_up(1, train_set)) / (len(consec_up_then_down(1, train_set)) + len(consec_up_then_up(1, train_set)))) * 100, '%')
    print('The probability after seeing 1 consecutive UP days, that the next day is an DOWN day is',
          (len(consec_up_then_down(1, train_set)) / (len(consec_up_then_down(1, train_set)) + len(consec_up_then_up(1, train_set)))) * 100, '%')

    print()
    print('FOR TICKER SPY:')
    print('The probability after seeing 3 consecutive UP days, that the next day is an UP day is',
          (len(consec_up_then_up(3, train_set_SP))/(len(consec_up_then_down(3, train_set_SP))+len(consec_up_then_up(3, train_set_SP))))*100, '%')
    print('The probability after seeing 3 consecutive UP days, that the next day is an DOWN day is',
          (len(consec_up_then_down(3, train_set_SP)) / (len(consec_up_then_down(3, train_set_SP)) + len(consec_up_then_up(3, train_set_SP)))) * 100, '%')

    print()
    print('The probability after seeing 2 consecutive UP days, that the next day is an UP day is',
          (len(consec_up_then_up(2, train_set_SP))/(len(consec_up_then_down(2, train_set_SP))+len(consec_up_then_up(2, train_set_SP))))*100, '%')
    print('The probability after seeing 2 consecutive UP days, that the next day is an DOWN day is',
          (len(consec_up_then_down(2, train_set_SP)) / (len(consec_up_then_down(2, train_set_SP)) + len(consec_up_then_up(2, train_set_SP)))) * 100, '%')

    print()
    print('The probability after seeing 1 consecutive UP days, that the next day is an UP day is',
          (len(consec_up_then_up(1, train_set_SP)) / (len(consec_up_then_down(1, train_set_SP)) + len(consec_up_then_up(1, train_set_SP)))) * 100, '%')
    print('The probability after seeing 1 consecutive UP days, that the next day is an DOWN day is',
          (len(consec_up_then_down(1, train_set_SP)) / (len(consec_up_then_down(1, train_set_SP)) + len(consec_up_then_up(1, train_set_SP)))) * 100, '%')

    print()
    print('----------Question 2----------')
    print()

    # Creating the testing set for PG
    print('FOR TICKER PG, TESTING SET')
    test_grouped = df.groupby(df.Year)
    test_set_2019 = test_grouped.get_group(2019)
    test_set_2020 = test_grouped.get_group(2020)

    test_set = test_set_2019._append(test_set_2020)
    print(test_set)

    # Creating the testing set for SPY
    print('FOR TICKER SPY, TESTING SET')
    test_grouped_SP = df2.groupby(df2.Year)
    test_set_2019_SP = test_grouped_SP.get_group(2019)
    test_set_2020_SP = test_grouped_SP.get_group(2020)

    test_set_SP = test_set_2019_SP._append(test_set_2020_SP)
    print(test_set_SP)

    prediction = []

    # Tests if a is a sublist of b
    def isSublist(a,b):
        pos = 0
        neg = 0
        #Adding a + to a, to see how many sequences there are in b that end with a +
        a.append('+')
        for i in range(len(b) - len(a)):
            if b[i:i+len(a)] == a:
                pos = pos + 1
        #Popping off the + we added
        a.pop()
        #Adding a - to a, to see how many sequences there are in b that end with a -
        a.append('-')
        for i in range(len(b)-len(a)):
            if b[i:i + len(a)] == a:
                neg = neg + 1
        #Popping off the -
        a.pop()

        if pos >= neg:
            #The next day will be positive.
            prediction.append('+')
        else:
            #The next day will be negative.
            prediction.append('-')


    # predicts the labels for the test set when given W (this is based on the training set).
    def predict_labels(W, tester, trainer):

        test = tester['True_Label'][0:W]
        test = test.tolist()
        # appends the first couple of labels to the prediction list. Whatever W is specified
        for p in range (0, W, 1):
            prediction.append(test[p])

        train_list = trainer['True_Label'].tolist()
        # For the length of the tester - W, create a sublist that is tested to be a sublist of the training set.
        for i in range(len(tester) - W):
            sub_test_set = tester['True_Label'][i:W+i]
            sub_test_list = sub_test_set.tolist()
            # Calls the method defined earlier for each i (it moves to the next sequence and tests if that sequence exists in the larger training set.
            isSublist(sub_test_list, train_list)
        return prediction

    # I had to set prediction empty before each call because I declared prediction earlier before both methods to allow
    # both methods to use it. This could be done better with one larger method so I could avoid these lines.
    prediction = []
    print('FOR TICKER PG:')
    print('When W = 2, here is the prediction list', predict_labels(2, test_set, train_set))
    prediction_w2 = prediction

    prediction = []
    print('When W = 3, here is the prediction list', predict_labels(3, test_set, train_set))
    prediction_w3 = prediction

    prediction = []
    print('When W = 4, here is the prediction list', predict_labels(4, test_set, train_set))
    prediction_w4 = prediction

    prediction = []
    print()
    print('FOR TICKER SPY:')
    print('When W = 2, here is the prediction list', predict_labels(2, test_set_SP, train_set_SP))
    prediction_w2_SP = prediction

    prediction = []
    print('When W = 3, here is the prediction list', predict_labels(3, test_set_SP, train_set_SP))
    prediction_w3_SP = prediction

    prediction = []
    print('When W = 4, here is the prediction list', predict_labels(4, test_set_SP, train_set_SP))
    prediction_w4_SP = prediction


    print()
    print('-----------Question 2 Part 2-----------')
    print()

    #Computes the accuracy of a prediction set
    def compute_accuracy (prediction_set, tester):
        true_count = 0
        false_count = 0
        test = tester['True_Label'][:]
        test_list = test.tolist()
        for i in range(len(test_list)):
            # if the value == the predicted value
            if test_list[i] == prediction_set[i]:
                # Then it's true!
                true_count = true_count + 1
            else:
                # If not, then its false
                false_count = false_count + 1
        return 'Accuracy =', (true_count/(false_count+true_count))*100, '%'

    print("FOR TICKER PG:")
    print('For W = 2...')
    print (compute_accuracy(prediction_w2, test_set))
    print('For W = 3...')
    print(compute_accuracy(prediction_w3, test_set))
    print('For W = 4...')
    print(compute_accuracy(prediction_w4, test_set))

    print()
    print("FOR TICKER SPY:")
    print('For W = 2...')
    print(compute_accuracy(prediction_w2_SP, test_set_SP))
    print('For W = 3...')
    print(compute_accuracy(prediction_w3_SP, test_set_SP))
    print('For W = 4...')
    print(compute_accuracy(prediction_w4_SP, test_set_SP))

    print()
    print('---------Question 3 Part 1-----------')
    print()

    # This method takes in 3 predictions and compares them, if two out of the three have +'s, it will append a + to the ensemble list,
    # if they don't, then it appends a -.
    def ensemble_learning(prediction_1, prediction_2, prediction_3):
        ensemble = []
        for i in range (len(prediction_1)):
            if prediction_1[i] == prediction_2[i] == '+' or prediction_2[i] == prediction_3[i] == '+' or prediction_1[i] == prediction_3[i] == '+':
                ensemble.append('+')
            else:
                ensemble.append('-')
        return ensemble

    ensemble_PG = ensemble_learning(prediction_w2, prediction_w3, prediction_w4)
    print('FOR TICKER PG:', ensemble_PG)
    print()
    ensemble_SP = ensemble_learning(prediction_w2_SP, prediction_w3_SP, prediction_w4_SP)
    print('FOR TICKER SPY:', ensemble_SP)

    print()
    print('--------Question 3 Part 2---------')
    print()
    print('FOR TICKER PG: (Ensemble)', compute_accuracy(ensemble_PG, test_set))
    print('FOR TICKER SPY: (Ensemble)', compute_accuracy(ensemble_SP, test_set_SP))

    print()
    print('--------Question 3 Part 3---------')
    print()

    # Computes the negative - label accuracy, if the value == the predicted value which needs to be a '-',
    # then add to the true_count, if not, add to the false count.
    def compute_neg_accuracy (prediction_set, tester):
        true_count = 0
        false_count = 0
        test = tester['True_Label'][:]
        test_list = test.tolist()
        for i in range(len(test_list)):
            if test_list[i] == prediction_set[i] == '-':
                true_count = true_count + 1
            else:
                false_count = false_count + 1
        return 'Accuracy of - labels=', (true_count/(false_count+true_count))*100, '%'


    # Computes the positive + label accuracy
    def compute_pos_accuracy (prediction_set, tester):
        true_count = 0
        false_count = 0
        test = tester['True_Label'][:]
        test_list = test.tolist()
        for i in range(len(test_list)):
            if test_list[i] == prediction_set[i] == '+':
                true_count = true_count + 1
            else:
                false_count = false_count + 1
        return 'Accuracy of + labels=', (true_count/(false_count+true_count))*100, '%'

    print('FOR TICKER PG: (Ensemble) Negative', compute_neg_accuracy(ensemble_PG, test_set))
    print('FOR TICKER SPY: (Ensemble) Negative', compute_neg_accuracy(ensemble_SP, test_set_SP))
    print('FOR TICKER PG: (Ensemble) Positive', compute_pos_accuracy(ensemble_PG, test_set))
    print('FOR TICKER SPY: (Ensemble) Positive', compute_pos_accuracy(ensemble_SP, test_set_SP))

    print()

    print("FOR TICKER PG NEGATIVE:")
    print('For W = 2...')
    print(compute_neg_accuracy(prediction_w2, test_set))
    print('For W = 3...')
    print(compute_neg_accuracy(prediction_w3, test_set))
    print('For W = 4...')
    print(compute_neg_accuracy(prediction_w4, test_set))

    print()
    print("FOR TICKER SPY NEGATIVE:")
    print('For W = 2...')
    print(compute_neg_accuracy(prediction_w2_SP, test_set_SP))
    print('For W = 3...')
    print(compute_neg_accuracy(prediction_w3_SP, test_set_SP))
    print('For W = 4...')
    print(compute_neg_accuracy(prediction_w4_SP, test_set_SP))

    print()
    print('---------Question 3 Part 4----------')
    print()

    print("FOR TICKER PG POSITIVE:")
    print('For W = 2...')
    print (compute_pos_accuracy(prediction_w2, test_set))
    print('For W = 3...')
    print(compute_pos_accuracy(prediction_w3, test_set))
    print('For W = 4...')
    print(compute_pos_accuracy(prediction_w4, test_set))

    print()
    print("FOR TICKER SPY POSITIVE:")
    print('For W = 2...')
    print(compute_pos_accuracy(prediction_w2_SP, test_set_SP))
    print('For W = 3...')
    print(compute_pos_accuracy(prediction_w3_SP, test_set_SP))
    print('For W = 4...')
    print(compute_pos_accuracy(prediction_w4_SP, test_set_SP))

    print()
    print('--------Question 4 Part 1----------')
    print()

    # Computes the true positives, true negatives, false postives, and false negatives (as well as TPR and TNR.)
    def compute_true_false(prediction_set, tester):
        true_pos_count = 0
        true_neg_count = 0
        false_pos_count = 0
        false_neg_count = 0
        test = tester['True_Label'][:]
        test_list = test.tolist()
        for i in range(len(test_list)):
            if test_list[i] == prediction_set[i] == '-':
                true_neg_count = true_neg_count + 1
            elif test_list[i] == prediction_set[i] == '+':
                true_pos_count = true_pos_count + 1
            elif test_list[i] != prediction_set[i]:
                if prediction_set[i] == '+' and test_list[i] == '-':
                    false_pos_count = false_pos_count+1
                elif prediction_set[i] == '-' and test_list[i] == '+':
                    false_neg_count = false_neg_count+1

        print('True Positives: ', true_pos_count)
        print('False Positives: ', false_pos_count)
        print('True Negatives: ', true_neg_count)
        print('False Negatives: ', false_neg_count)
        print('TPR: ', true_pos_count/(true_pos_count+false_neg_count))
        print('TNR: ', true_neg_count / (true_neg_count + false_pos_count))
        print()

    print("FOR TICKER PG:")
    print('W = 2...')
    compute_true_false(prediction_w2, test_set)
    print('W = 3...')
    compute_true_false(prediction_w3, test_set)
    print('W = 4...')
    compute_true_false(prediction_w4, test_set)
    print('Ensemble...')
    compute_true_false(ensemble_PG, test_set)

    print()

    print("FOR TICKER SPY:")
    print('W = 2...')
    compute_true_false(prediction_w2_SP, test_set_SP)
    print('W = 3...')
    compute_true_false(prediction_w3_SP, test_set_SP)
    print('W = 4...')
    compute_true_false(prediction_w4_SP, test_set_SP)
    print('Ensemble...')
    compute_true_false(ensemble_SP, test_set_SP)

    print()
    print("--------Question 5---------")
    print()

    # Buy and hold method that will return a list of how your money went up or down with each day
    # Prints the money total you will end up with using this test_set.
    def buy_and_hold(money_total, test_set):
        buyhold = []
        money = []
        returns = test_set['Return'][:].tolist()
        # For every day, you will be holding.
        for i in range(len(test_set)):
            buyhold.append(returns[i])
        for i in buyhold:
            money_total = (money_total*i)+money_total
            money.append(money_total)
        print(round(money_total, 2))
        return money

    print('Buying and holding with PG: ')
    buyhold_PG = buy_and_hold(100, test_set)
    print('Buying and holding with SPY: ')
    buyhold_SP = buy_and_hold(100, test_set_SP)

    # Will return a list of the value of your money day by day if you plan to trade based on a prediction set.
    # Prints out the value you end up with on the last day
    def prediction_trading(money_total, test_set, prediction):
        trade = []
        money = []
        returns = test_set['Return'][:].tolist()
        for i in range(len(prediction)):
            if prediction[i] == '+':
                trade.append(returns[i])
            elif prediction[i] == '-':
                trade.append(0)
        for i in trade:
            money_total = (money_total*i)+money_total
            money.append(money_total)
        print(round(money_total, 2))
        return money

    print()
    print('FOR TICKER PG:')
    print('W=3 Trading strategy yields = ')
    trade_w3_PG = prediction_trading(100, test_set, prediction_w3)
    print('Ensemble Trading strategy yields = ')
    trade_ensemble_PG = prediction_trading(100, test_set, ensemble_PG)

    print()

    print('FOR TICKER SPY:')
    print('W=2 Trading strategy yields = ')
    trade_w2_SP = prediction_trading(100, test_set, prediction_w2_SP)
    print('Ensemble Trading strategy yields = ')
    trade_ensemble_SP = prediction_trading(100, test_set, ensemble_SP)

    # Plots graphs based on two strategies.
    def plot_graphs(test_set, trade_set, label1, buyhold, label2, Title ):

        index = []
        dates = test_set['Date'][:].tolist()

        for i in range(len(dates)):
            index.append(dates[i])

        index = pd.to_datetime(index)
        plt.plot(index, trade_set, label=label1)
        plt.plot(index, buyhold, label=label2)
        plt.legend()
        # Formats the dates
        plt.gcf().autofmt_xdate()
        plt.title(Title)
        plt.xlabel('Trading Dates')
        plt.ylabel('Money $')
        plt.show()

    # Plots the graphs for question 5.

    plot_graphs(test_set, trade_w3_PG, 'W=3', buyhold_PG, 'BuyHold','TICKER PG: W=3 and Buy and Hold, Money Made vs Trading Dates')
    plot_graphs(test_set, trade_ensemble_PG,'Ensemble', buyhold_PG,'BuyHold', 'TICKER PG: Ensemble and Buy and Hold, Money Made vs Trading Dates')

    plot_graphs(test_set, trade_w2_SP, 'W=2',buyhold_SP, 'BuyHold', 'TICKER SPY: W=2 and Buy and Hold, Money Made vs Trading Dates')
    plot_graphs(test_set, trade_ensemble_SP, 'Ensemble', buyhold_SP, 'BuyHold', 'TICKER SPY: Ensemble and Buy and Hold, Money Made vs Trading Dates')

except Exception as e:
    print(e)
    print('failed to read stock data for ticker: ', ticker)
















