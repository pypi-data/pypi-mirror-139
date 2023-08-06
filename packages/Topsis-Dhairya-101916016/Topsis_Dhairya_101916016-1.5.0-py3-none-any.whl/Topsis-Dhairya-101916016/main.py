#Version of Module

__version__ = "1.0.0"

#Importing libraries
import pandas as pd
import numpy as np
import sys


# Checking for numerical values only
def checkfornumerical(_df):
    if _df.shape[1] == _df.select_dtypes(include=np.number).shape[1]:
        return True
    else:
        return False


# Normalising the dataset
def normalize(_evaldf):
    for i in range(_evaldf.shape[1]):
        rootofsums = 0
        for j in range(_evaldf.shape[0]):
            rootofsums = rootofsums + _evaldf.iloc[j, i] ** 2
        rootofsums = rootofsums ** 0.5
        for j in range(_evaldf.shape[0]):
            _evaldf.iloc[j, i] = (_evaldf.iloc[j, i] / rootofsums)
    return _evaldf


# Adding weights to the dataset
def addingweights(_evaldf, _weights):
    weights = _weights.split(",")
    if len(weights) != _evaldf.shape[1]:
        # Throw error & log it - if weights are not equal to columns
        print("Size of weights is not equal to number of columns")
        sys.exit()

    for i in range(len(weights)):
        try:
            weights[i] = float(weights[i])
        except:
            # Throw error & log it - if weights are not int
            print("Value of weight is not in float. Please enter only float value.")
            sys.exit()

    for i in range(_evaldf.shape[1]):
        for j in range(_evaldf.shape[0]):
            _evaldf.iloc[j, i] = (_evaldf.iloc[j, i]) * (weights[i])

    return _evaldf


# Finding ideal best and ideal worst in dataset
def idealbestworst(_evaldf, _impacts):
    impacts = _impacts.split(",")
    if len(impacts) != _evaldf.shape[1]:
        # Throw error & log it - if impacts are not equal to columns
        print("Size of Impacts is not equal to number of columns")
        sys.exit()
    for i in range(len(impacts)):
        if impacts[i] == '+' or impacts[i] == '-':
            continue
        else:
            # Throw error & log it - if impacts are not + or -
            print("Impacts are not '+' or '-'")
            sys.exit()
    idealbest = []
    idealworst = []
    for i in range(_evaldf.shape[1]):
        if impacts[i] == "+":
            idealbest.append(max(_evaldf.iloc[:, i]))
            idealworst.append(min(_evaldf.iloc[:, i]))
        if impacts[i] == "-":
            idealbest.append(min(_evaldf.iloc[:, i]))
            idealworst.append(max(_evaldf.iloc[:, i]))

    _evaldf.loc[len(_evaldf.index)] = idealbest
    _evaldf.loc[len(_evaldf.index)] = idealworst
    return _evaldf


# Finding Euclidean Distance in dataset
def euclideandistance(_evaldf):
    idealbest = list(_evaldf.iloc[-2, :])
    idealworst = list(_evaldf.iloc[-1, :])
    _evaldf = _evaldf.iloc[:-2, :].copy()

    edp = []
    edn = []

    for i in range(_evaldf.shape[0]):
        tempedp = 0
        tempedn = 0
        for j in range(_evaldf.shape[1]):
            tempedp = tempedp + (_evaldf.iloc[i, j] - idealbest[j]) ** 2
            tempedn = tempedn + (_evaldf.iloc[i, j] - idealworst[j]) ** 2
        edp.append(tempedp ** 0.5)
        edn.append(tempedn ** 0.5)

    _evaldf["edp"] = edp
    _evaldf["edn"] = edn
    _evaldf["edp+edn"] = _evaldf["edp"] + _evaldf["edn"]

    pscore = []

    for i in range(_evaldf.shape[0]):
        pscore.append(((_evaldf["edn"][i]) / (_evaldf["edp+edn"][i])) * 100)

    _evaldf["Topsis Score"] = pscore

    return _evaldf


# Giving ranks in dataset
def givingranks(_evaldf):
    mapping = {}
    temp_psscore = list(_evaldf.iloc[:, -1])
    temp_psscore.sort(reverse=True)

    for i in range(len(temp_psscore)):
        mapping[temp_psscore[i]] = i + 1

    ranks = []

    for i in range(_evaldf.shape[0]):
        ranks.append(mapping[_evaldf.iloc[i, -1]])

    _evaldf = _evaldf.copy()
    _evaldf["Rank"] = ranks

    return _evaldf


#main topsis code
def topsis(_inputcsv,_weights,_impacts,_resultfilename):
  try:
    df = pd.read_csv(_inputcsv)
  except:
    print("Input file could not be found")
    sys.exit()

  #Checking if number of columns is atleast 3
  if len(df.columns) < 3:
    print("There needs to be atleast 3 columns")
    sys.exit()

  #Checking for numerical values only
  if checkfornumerical(df.iloc[:,1:]) == False:
    print("Need only numerical values")
    sys.exit()

  evaldf = df.iloc[:,1:]
  weights = _weights
  impacts = _impacts
  evaldf1 = normalize(evaldf)
  evaldf2 = addingweights(evaldf1,weights)
  evaldf3 = idealbestworst(evaldf2,impacts)
  evaldf4 = euclideandistance(evaldf3)
  evaldf5 = givingranks(evaldf4)
  df["Topsis Score"] = evaldf5["Topsis Score"]
  df["Rank"] = evaldf5["Rank"]
  df.to_csv(_resultfilename,index=False)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Not enough arguments provided")
        sys.exit()

    infilename = sys.argv[1]
    weights = sys.argv[2]
    impacts = sys.argv[3]
    outfilename = sys.argv[4]

    topsis(infilename, weights, impacts, outfilename)