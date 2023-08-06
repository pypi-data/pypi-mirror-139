import pandas as pd
from pandas.api.types import is_numeric_dtype
import os
import sys
import math


def main():

    # check for input syntax
    if len(sys.argv) != 5:
        print("Incorrect Input!")
        print(
            "Syntax: python <program.py> <InputDataFile> <Weights> <imps> <ResultFileName>")
        exit(1)

    # check if file exist
    elif not os.path.isfile(sys.argv[1]):
        print("File doesn't exist!")
        exit(1)

    else:
        df = pd.read_csv(sys.argv[1])
        df_copy = df.copy()
        # converting char to integer and spliting along ','
        w = [int(i) for i in sys.argv[2].split(',')]
        # spliting along ','
        imp = sys.argv[3].split(',')
        cols = len(df.columns)

        # check for column size
        if cols < 3:
            print("Column Size should be greater than 3!")
            exit(1)

        # check of number of columns in weights and imps are same or not
        if cols-1 != len(w) or cols-1 != len(imp):
            print("Size of impact/weight doesn't match the input file size!")
            exit(1)

        # check if any value other than + or - is present in impact array
        for i in imp:
            if not (i == '+' or i == '-'):
                print("Impact array can only contain + or -")
                exit(1)

        # check for numeric values
        for column in df:
            if column != 'Fund Name':
                if is_numeric_dtype(df[column]) is False:
                    print("Column should only contain numeric values!")
                    exit(1)

        topsis(df_copy, df, cols, w, imp)


def topsis(df_copy, df, cols, weights, imp):

    # normalizing the array
    for column in df_copy:
        if column != 'Fund Name':
            df_copy[column] = df_copy[column] / \
                math.sqrt(df_copy[column].pow(2).sum())

    # calculating V1 and V2 according to impacts
    V1 = (df_copy.max())[1:]
    V2 = (df_copy.min())[1:]
    for i in range(0, cols-1):
        if imp[i] == '-':
            V1[i] = V2[i]
            V2[i] = V1[i]

    # calculating topsis score
    score = []
    for i in range(len(df_copy)):
        S1, S2 = 0, 0
        for j in range(1, cols):
            S1 = S1 + (V1[j-1] - df_copy.iloc[i, j])**2
            S2 = S2 + (V2[j-1] - df_copy.iloc[i, j])**2
        S1 = math.sqrt(S1)
        S2 = math.sqrt(S2)
        score.append(S2/(S1 + S2))
    df['Topsis Score'] = score

    # calculate rank from topsis score
    df['Rank'] = (df['Topsis Score'].rank(
        method='max', ascending=False))
    df = df.astype({"Rank": int})

    # convert df to csv
    df.to_csv(sys.argv[4], index=False)


if __name__ == "__main__":
    main()
