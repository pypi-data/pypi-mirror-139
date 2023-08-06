import pandas as pd
import os
import sys


def main(): 
    
    if len(sys.argv) != 5:
        print("ERROR : Incorrect number of parameters")
        print("USAGE : python topsis.py inputfile.csv '1,1,1,1,1' '+,+,-,+,+' result.csv")
        sys.exit()

    elif not os.path.isfile(sys.argv[1]):
        print("ERROR :" ,sys.argv[1], "Don't exist!!")
        sys.exit()

    
    elif ".csv" != (os.path.splitext(sys.argv[1]))[1]:
        print("ERROR :",sys.argv[1], "is not a csv file!!")
        sys.exit()

    else:
        dataset, temp_dataset = pd.read_csv(
            sys.argv[1]), pd.read_csv(sys.argv[1])
        numberOfCol = len(temp_dataset.columns.values)

        
        if numberOfCol < 3:
            print("ERROR : Input file have less then 3 columns")
            sys.exit()

        
        for i in range(1, numberOfCol):
            pd.to_numeric(dataset.iloc[:, i], errors='coerce')
            dataset.iloc[:, i].fillna(
                (dataset.iloc[:, i].mean()), inplace=True)

        
        try:
            weights = [int(i) for i in sys.argv[2].split(',')]
        except:
            print("ERROR : Check weights array and retry")
            sys.exit()
        impact = sys.argv[3].split(',')
        for i in impact:
            if not (i == '+' or i == '-'):
                print("ERROR : Check Impact array and retry")
                sys.exit()

        
        if numberOfCol != len(weights)+1 or numberOfCol != len(impact)+1:
            print(
                "ERROR : Number of weights, impacts and columns are not the same")
            sys.exit()

        if (".csv" != (os.path.splitext(sys.argv[4]))[1]):
            print("ERROR : Output file extension is wrong")
            sys.exit()
        if os.path.isfile(sys.argv[4]):
            os.remove(sys.argv[4])
        
        topsis_pipy(temp_dataset, dataset, numberOfCol, weights, impact)


def Normalize(temp_dataset, numberOfCol, weights):        
    for i in range(1, numberOfCol):
        temp = 0
        for j in range(len(temp_dataset)):
            temp = temp + temp_dataset.iloc[j, i]**2
        temp = temp**0.5
        for j in range(len(temp_dataset)):
            temp_dataset.iat[j, i] = (
                temp_dataset.iloc[j, i] / temp)*weights[i-1]
    return temp_dataset


def Calcn(temp_dataset, numberOfCol, impact):
    posit = (temp_dataset.max().values)[1:]
    negit = (temp_dataset.min().values)[1:]
    for i in range(1, numberOfCol):
        if impact[i-1] == '-':
            posit[i-1], negit[i-1] = negit[i-1], posit[i-1]
    return posit, negit


def topsis_pipy(temp_dataset, dataset, numberOfCol, weights, impact):
    temp_dataset = Normalize(temp_dataset, numberOfCol, weights)
    posit, negit = Calcn(temp_dataset, numberOfCol, impact)

    score = []
    for i in range(len(temp_dataset)):
        temp_p, temp_n = 0, 0
        for j in range(1, numberOfCol):
            temp_p = temp_p + (posit[j-1] - temp_dataset.iloc[i, j])**2
            temp_n = temp_n + (negit[j-1] - temp_dataset.iloc[i, j])**2
        temp_p, temp_n = temp_p**0.5, temp_n**0.5
        score.append(temp_n/(temp_p + temp_n))
    dataset['Topsis Score'] = score
    
    dataset['Rank'] = (dataset['Topsis Score'].rank(
        method='max', ascending=False))
    dataset = dataset.astype({"Rank": int})
    
    dataset.to_csv(sys.argv[4], index=False)

if __name__ == "__main__":
    main()
    