import pandas as pd
import sys

def topsis(inpFile, w, imp):

    if not(inpFile.endswith('.csv')):
        print('Incorrect file type, csv files allowed.')
        sys.exit()

    try:
        topsis_df = pd.read_csv(inpFile)
    except:
        print('File not Found')
        sys.exit()

    if len(topsis_df.columns)<3:
        print('Input file must contain more than or equal to three columns.')
        sys.exit()

    df = topsis_df.drop('Fund Name',axis=1)
    df.apply(lambda s: pd.to_numeric(s, errors='raise').notnull().all())

    rootSumSquares = []
    for i in df.columns:
        sum = 0
        for j in df[i]:
            sum += (j**2)
        sum = sum**0.5
        rootSumSquares.append(sum)

    j=0
    for i in df.columns:
        df[i]/=rootSumSquares[j]
        j = j+1

    weights = w
    weights = list(weights.split(','))
    if not(all(map(str.isdigit, weights))):
        print('Weights should be numeric and should be separated by commas(,).')
        sys.exit()
    weights = list(map(int, weights))

    impacts = imp
    impacts = list(impacts.split(','))

    if(len(impacts)!=len(df.columns) or (len(weights)!=len(df.columns))):
        print('Number of weights, number of impacts and number of columns must be same.')
        sys.exit()

    j=0
    for i in df.columns:
        df[i] *= weights[j]
        j = j+1

    idlBest = []
    idlWorst = []
    j=0
    for i in df.columns:
        if impacts[j]=='+':
            idlBest.append(max(df[i]))
            idlWorst.append(min(df[i]))
        elif impacts[j]=='-':
            idlBest.append(min(df[i]))
            idlWorst.append(max(df[i]))
        else:
            print('Impacts must be either + or - and should be separated by commas(,)')
            sys.exit()
        j=j+1

    eucBest = []
    eucWorst = []
    for i in range(len(df)):
        temp1=0
        temp2=0
        for j in range(len(df.columns)):
            temp1 += (df.iloc[i,j]-idlBest[j])**2
            temp2 += (df.iloc[i,j]-idlWorst[j])**2

        eucBest.append(temp1**0.5)
        eucWorst.append(temp2**0.5)

    topsis_score = []
    for i in range(len(df)):
        topsis_score.append(eucWorst[i]/(eucBest[i]+eucWorst[i]))

    topsis_df['Topsis Score'] = topsis_score
    topsis_df['Rank'] = topsis_df['Topsis Score'].rank(ascending=False)

    print(topsis_df)

# topsis('101903326-data.csv', '1,1,1,1,1', '+,+,+,-,+')

