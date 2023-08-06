import pandas as pd
import numpy as np
import sys
import math


def calculate_rms(root_mean_square, nrow, ncol, df):
    for i in range(0, nrow):
        for j in range(0, ncol):
            root_mean_square[j] += (df[i][j] * df[i][j])
    for i in range(0, ncol):
        root_mean_square[i] = math.sqrt(root_mean_square[i])
    return root_mean_square


def weighted_normalized_decision_matrix(df, ncol, nrow, weights):
    for i in range(nrow):
        for j in range(ncol):
            df[i][j] = df[i][j] * weights[j]
    return df


def Plus_distance(maxData, df, nrow, ncol):
    list = []
    for i in range(0, nrow):
        sum = 0
        for j in range(0, ncol):
            sum += pow((df[i][j] - maxData[j]), 2)
        list.append(float(pow(sum, 0.5)))
    return list


def Minus_distance(minData, df, nrow, ncol):
    list = []
    for i in range(0, nrow):
        sum = 0
        for j in range(0, ncol):
            sum += pow((df[i][j] - minData[j]), 2)
        list.append(float(pow(sum, 0.5)))
    return list


def main():
    if len(sys.argv) != 5:
        print("Invalid number of parameters")
        exit(0)

    try:
        weights = []
        impacts = []
        for i in sys.argv[2]:
            if i != ',':
                weights.append(float(i))
        for i in sys.argv[3]:
            if i != ',':
                impacts.append(str(i))
    except:
        print('Wrong input for weights and impacts')
        print('They must be separated by commas ')
        exit(0)

    for s in impacts:
        if s not in ('+', '-'):
            print('Wrong input for impacts')
            exit(0)

    output_file = sys.argv[4]

    try:
        data = pd.read_csv(sys.argv[1])
    except:
        print('File not found')
        exit(0)

    if len(list(data.columns)) < 3:
        print('Input file must contain 3 or more columns')
        exit(0)

    df = data.drop(['Fund Name'], axis=1)
    nrow = df.shape[0]
    ncol = df.shape[1]

    if len(weights) != ncol or len(impacts) != ncol:
        print("Incorrect number of weights or impacts")
        exit(0)

    # Step 1
    df = df.values.astype(float)
    weight_sum = np.sum(weights)

    # Step 2 - Vector normalization
    # Step 2.1 and Step 2.2
    root_mean_square = [0] * ncol
    normalized_performance = []
    normalized_performance = calculate_rms(root_mean_square, nrow, ncol, df)
    for i in range(0, nrow):
        for j in range(0, ncol):
            df[i][j] = (df[i][j] / normalized_performance[j])

    # Weight Assignment
    # Step 3.1 - Weight assignment is by command line (Calculating normalized weight)
    for i in range(ncol):
        weights[i] /= weight_sum

    # Step 3.2 - Weight * Normalized performance value
    normalized_matrix = weighted_normalized_decision_matrix(df, ncol, nrow, weights)

    # Step 4 - Find Ideal best and Ideal worst
    maxData = np.amax(df, axis=0)
    minData = np.amin(df, axis=0)
    for i in range(len(impacts)):
        if impacts[i] == '-':
            maxData[i], minData[i] = minData[i], maxData[i]

    # Step 5 - Calculate Euclidean Distance
    euclidPlus = []
    euclidMinus = []
    euclidPlus = Plus_distance(maxData, df, nrow, ncol)
    euclidMinus = Minus_distance(minData, df, nrow, ncol)

    # Step 6 - Calculate Performance score
    performance_score = {}
    value = []
    for i in range(0, nrow):
        performance_score[i + 1] = euclidMinus[i] / (euclidMinus[i] + euclidPlus[i])
        value.append(performance_score[i + 1])
    ans = sorted(list(performance_score.values()), reverse=True)
    rank = {}
    for val in value:
        rank[(ans.index(val) + 1)] = val
    result = data
    result['Topsis Score'] = list(rank.values())
    result['Rank'] = list(rank.keys())

    output = pd.DataFrame(result)
    output.to_csv(output_file, index=False)


if __name__ == "__main__":
    main()
