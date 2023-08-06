# ***************************************************************************
# By Vyom Chopra
# A package to generate topsis score and rank in mere moments

import numpy as np
import pandas as pd

# ***************************************************************************
# Function to get the numeric columns indexes
def getNumeric(dataset):

    # Getting the numeric-only columns of dataframe
    useful = 'int32 int64 float32 float64'.split()
    dtype = dataset.dtypes.tolist()
    idx_numeric = []
    for ind,i in enumerate(dtype):
        if i in useful:
            idx_numeric.append(ind)

    # fetching the columns names by index from the idx_numeric
    columns_list = dataset.columns.tolist()
    non_numeric_columns_list = [columns_list[i] for i in idx_numeric]

    return non_numeric_columns_list

# ***************************************************************************
# Function to check the contents of weights and impact lists
def checkWI(dataset_col_len, weights, choose):

    # Checking whether all the lengths of weigths, impacts and columns are equal
    x = len(weights)
    y = len(choose)
    z = dataset_col_len
    if x != y or y != z or z != x:
        raise Exception("Lengths of weights, choices and dataframe columns are not equal")

    # checking the contents of impacts
    ava_impact = '+ -'.split()
    for i in choose:
        if i not in ava_impact:
            raise Exception("One or more elements of the impacts is not +/-")

# ***************************************************************************
# Function to normalize the values
def Normalization(df,weights):
    for i in range(df.shape[1]):
        total_sq_sum = 0
        
        for j in list(df.iloc[:,i]):
            total_sq_sum += j**2
        deno = total_sq_sum**0.5
        
        for ind,k in enumerate(list(df.iloc[:,i])):
            df.iloc[ind,i] = k*weights[i]/deno


# ***************************************************************************
# function for calculating ideal best and ideal worst
def calcIdeal(df,choose):
    ideal_best = []
    ideal_worst = []
    
    for i in range(df.shape[1]):
        if choose[i] == '+':
            ideal_best.append(df.max()[i])
            ideal_worst.append(df.min()[i])
        else:
            ideal_best.append(df.min()[i])
            ideal_worst.append(df.max()[i])
            
    return ideal_best,ideal_worst

# ***************************************************************************
# function for calculating topsis score
def topsisScore(df,ideal_best,ideal_worst):
    dist_pos = []
    dist_neg = []
    for i in range(df.shape[0]):
            dist_pos.append(np.linalg.norm(df.iloc[i,:].values-ideal_best))
            dist_neg.append(np.linalg.norm(df.iloc[i,:].values-ideal_worst))

    score = []
    for i in range(len(dist_pos)):
        score.append(dist_neg[i]/(dist_pos[i]+dist_neg[i]))
    
    return score

# ***************************************************************************
# function for adding the rank column
def add_topsis(dataset,score):
    # Adding the rank and score columns in the original dataset
    dataset['Topsis Score'] = score
    dataset['Rank'] = (dataset['Topsis Score'].rank(method='max', ascending=False))
    dataset = dataset.astype({"Rank": int})


# ***************************************************************************
def build_topsis(dataset, weights, choose):

    try:
        if(len(dataset) == 0):
            raise Exception("No records are present in the given dataframe.")

        # get the list of numeric columns
        non_numeric_columns_list = getNumeric(dataset)
        # making a copy of the dataset with only the numeric columns
        # copying because we need to return the topsis score column in the original dataset
        df = dataset.loc[:,dataset.columns.isin(non_numeric_columns_list)].copy()

        # Check for no of columns
        if len(df.columns.tolist()) <= 1:
            raise Exception("Columns are less or equal to one. Data insufficient to calculate topsis.")
        
        # check the contents of weights and impacts lists
        checkWI(len(df.columns.tolist()), weights, choose)

        # Calling the normalization function    
        Normalization(df,weights)

        # Calling the calcIdeal function
        ideal_best,ideal_worst = calcIdeal(df,choose)

        # Calling the topsis score generator function
        score = topsisScore(df,ideal_best,ideal_worst)

        # Adding the rank column according to the topsis score
        add_topsis(dataset,score)

        # returning the dataset
        return dataset
    
    except Exception as e:
        print(f"{type(e).__name__} was raised: {e}")

# By Vyom Chopra
# ***************************************************************************
if __name__ == "__main__":

    data = pd.read_csv("sample_data.csv")
    weights = [1,1,2,1]
    impacts = ["+","+","-","+"]
    dataset = build_topsis(data,weights,impacts)
    print(dataset)

# ***************************************************************************