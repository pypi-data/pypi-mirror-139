import pandas as pd
import numpy as np
import sys
import os


def topsis(input_file, weights_inp, impacts_inp, res_file):
    if not os.path.isfile(input_file):
        print(f"{input_file} Don't exist!!")
        exit(1)

    if ".csv" != (os.path.splitext(input_file))[1]:
        print(f"{sys.argv[1]} is not csv!!")
        exit(1)

    try:
        data, df = pd.read_csv(input_file), pd.read_csv(input_file)

    except:
        print("Error while reading")
        exit(1)

    nCol = len(data.columns.values)

    if nCol < 3:
        print("Input file have less then 3 columns")
        exit(1)

    vals = input_file
    weights = input_file


    try:
        for i in range(1, nCol):
            pd.to_numeric(df.iloc[:, i],errors='coerce')
    except:
        print("Error : From 2nd to last columns must contain numeric values only    ")
        exit(1)

    try:
        vals = [float(i) for i in weights_inp.split(',')]

    except:
        print("In weights array please check again")
        exit(1)

    weights = impacts_inp.split(',')




    for i in weights:
        if not (i == '+' or i == '-'):
            print("In impact array please check again")
            exit(1)

    if nCol != len(vals) + 1 or nCol != len(weights) + 1:
        print("Number of weights, number of impacts and number of columns not same")
        exit(1)

    if (".csv" != (os.path.splitext(res_file))[1]):
        print("Output file extension is wrong")
        exit(1)

    if os.path.isfile(res_file):
        os.remove(res_file)

    # In[82]:

    # vals= "1,1,1,1,1"
    # weights="+,+,+,+,+"
    # # impact=weights
    # # weights=vals

    #     df=data.copy()
    df = df.iloc[:, 1:]
    for i in df.columns:
        x = df[i] * df[i]
        sq_sum = x.sum()
        sq_sum = sq_sum ** 0.5
        df[i] /= sq_sum

    # weights=weights.split(',')
    # vals=vals.split(',')

    vals = [float(numeric_string) for numeric_string in vals]

    # execetion
    if (len(vals) != len(weights)):
        exit()
    # print(len(vals))
    count = 0
    for i in df.columns:
        df[i] *= vals[count]
        count += 1

    # # print(df)
    # #3rd step
    max_list = []
    min_list = []

    count = 0
    for i in df.columns:
        maax = max(df[i])
        miin = min(df[i])
        if (weights[count] == '-'):
            t = maax
            maax = miin
            miin = t

        max_list.append(maax)
        min_list.append(miin)
        count += 1

    # print(max_list)
    # print(min_list)

    max_list = [float(numeric_string) for numeric_string in max_list]
    min_list = [float(numeric_string) for numeric_string in min_list]

    s_max = []
    s_min = []

    ct = 0

    for j in df.index:
        ct = 0
        sumx = 0
        sumy = 0
        for i in df.columns:
            temp_max = df[i][j] - max_list[ct]
            temp_min = df[i][j] - min_list[ct]
            sumy += temp_min * temp_min
            sumx += temp_max * temp_max
            ct += 1

        s_max.append(sumx ** 0.5)
        s_min.append(sumy ** 0.5)

    # print(s_max)
    # print(s_min)

    # In[83]:

    aa = []
    for i in range(len(s_max)):
        ax = s_min[i] / (s_min[i] + s_max[i])
        aa.append(ax)

    # print(aa)

    # In[85]:

    data['Topsis Score'] = aa
    data['Rank'] = data['Topsis Score'].rank(ascending=0).astype(np.int32)

    data.to_csv(res_file, index=False)
    return data







