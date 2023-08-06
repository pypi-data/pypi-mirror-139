import pandas as pd
import os
import sys


def main():
    if len(sys.argv) != 5:
        print("INCORRECT NUMBER OF PARAMETERS")
        exit(1)

    elif not os.path.isfile(sys.argv[1]):
        print(f"{sys.argv[1]} Don't exist!!")
        exit(1)

    else:
        df=pd.read_csv(sys.argv[1])
        df1=pd.read_csv(sys.argv[1])
        cols = len(df1.columns.values)

        if cols < 3:
            print("LESS THAN 3 COLUMNS")
            exit(1)

        for i in range(1, cols):
            pd.to_numeric(df.iloc[:, i], errors='coerce')
            df.iloc[:, i].fillna((df.iloc[:, i].mean()), inplace=True)

        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("Weights error")
            exit(1)
        impacts = sys.argv[3].split(',')
        for i in impacts:
            if not (i == '+' or i == '-'):
                print("Impacts errors")
                exit(1)

        if cols != len(weights)+1 or cols != len(impacts)+1:
            print("Number of weights,impacts and columns not same")
            exit(1)

        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        TOPSIS(df1, df, cols, weights, impacts)

def Evaluate(df1, cols, impact):
    a = (df1.max().values)[1:]
    b = (df1.min().values)[1:]
    for i in range(1, cols):
        if impact[i-1] == '-':
            a[i-1], b[i-1] = b[i-1], a[i-1]
    return a, b

def Normalization(df1, cols, weights):
    for i in range(1, cols):
        temp = 0
        for j in range(len(df1)):
            temp = temp + df1.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(df1)):
            df1.iat[j, i] = (df1.iloc[j, i] / temp)*weights[i-1]
    return df1

def TOPSIS(df1, df, cols, weights, impact):
    df1 = Normalization(df1, cols, weights)
    a, b = Evaluate(df1, cols, impact)
    score = []
    for i in range(len(df1)):
        temp_a, temp_b = 0, 0
        for j in range(1, cols):
            temp_a = temp_a + (a[j-1] - df1.iloc[i, j])**2
            temp_b = temp_b + (b[j-1] - df1.iloc[i, j])**2
        temp_a, temp_b = temp_a**0.5, temp_b**0.5
        score.append(temp_b/(temp_a + temp_b))
    df['Topsis Score'] = score

    df['Rank'] = (df['Topsis Score'].rank(method='max', ascending=False))
    df = df.astype({"Rank": int})

    df.to_csv(sys.argv[4], index=False)
    
if __name__ == "__main__":
    main()