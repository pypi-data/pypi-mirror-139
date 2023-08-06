import pandas as pd
import os
import sys

def Topsis(input_file, weight_string, impact_string, output_file):
    # Handling input file errors
    if not os.path.isfile(input_file):
        print(f"Input File {input_file} doesn't exist!!")
        exit(1)
    if (os.path.splitext(input_file))[1] != ".csv":
        print(f"Invalid input file extension. {input_file} is not csv!!")
        exit(1)

    # reading dataset and checking for errors
    original_df = pd.read_csv(input_file)
    df = original_df.copy()
    nCol = len(original_df.columns.values)
    nRows = len(original_df)
    useful_nCol = nCol-1
    if nCol < 3:
        print(f"Input File {input_file} have less then 3 columns")
        exit(1)

    # Handling weight string errors
    try:
        weights = []
        for i in weight_string.split(','):
            weights.append(int(i))
    except:
        print("Invalid weight string, please check again")
        exit(1)
    if useful_nCol != len(weights):
        print("Number of weights and number of columns are not same")
        exit(1)

    # Handling impact string errors
    try:
        impact = []
        for i in impact_string.split(','):
            if not (i == '+' or i == '-'):
                raise Exception
            impact.append(i)
    except:
        print("Invalid impact string, please check again")
        exit(1)
    if useful_nCol != len(impact):
        print("Number of impacts and number of columns are not same")
        exit(1)

    # Handling output file errors
    if ".csv" != (os.path.splitext(output_file))[1]:
        print(f"Invalid output file extension. {output_file} is not csv!!")
        exit(1)

    # normalising the dataset
    for i in range(1, nCol):
        temp = 0
        for j in range(nRows):
            temp += (df.iat[j, i]**2)
        temp **= 0.5
        for j in range(nRows):
            df.iat[j, i] /= temp
            df.iat[j, i] *= weights[i-1]

    # calculating positive and negative values
    col_max = (df.max().values)[1:]
    col_min = (df.min().values)[1:]
    p_values = []
    n_values = []
    for i in range(1, nCol):
        if impact[i-1] == '-':
            p_values.append(col_min[i-1])
            n_values.append(col_max[i-1])
        if impact[i-1] == '+':
            p_values.append(col_max[i-1])
            n_values.append(col_min[i-1])

    # calculating topsis score
    topsis_score = []
    for i in range(nRows):
        p_colScore = 0
        n_colScore = 0
        for j in range(1, nCol):
            p_colScore += (p_values[j-1] - df.iloc[i, j])**2
            n_colScore += (n_values[j-1] - df.iloc[i, j])**2
        p_colScore **= 0.5
        n_colScore **= 0.5
        topsis_score.append(n_colScore/(p_colScore + n_colScore))
    original_df['Topsis Score'] = topsis_score

    # assigning rank on the basis of topsis score
    original_df['Rank'] = (original_df['Topsis Score'].rank(
        method='max', ascending=False))
    original_df = original_df.astype({"Rank": int})

    # writing dataset to output file
    original_df.to_csv(output_file, index=False)
