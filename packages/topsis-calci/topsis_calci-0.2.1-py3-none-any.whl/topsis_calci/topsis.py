import numpy as np
import pandas as pd

from .validators import data_validations

def _normalize(df: pd.DataFrame):
    for col in df.columns:
        squared_sum = (df[col]**2).sum()
        sqrt_squared_sum = squared_sum ** (1/2)
        df[col] = df[col] / sqrt_squared_sum

def _add_weights(df, weights):
    sm = sum(weights)
    weights = [w / sm for w in weights]
    for i in range(len(weights)):
        df.iloc[:, i] = df.iloc[:, i]*weights[i]

def _get_best_and_worst(df, impacts):
    best = []
    worst = []

    for i in range(len(impacts)):
        mn = df.iloc[:,i].min()
        mx = df.iloc[:,i].max()
        
        if impacts[i] == '+':
            best.append(mx)
            worst.append(mn)
        else:
            best.append(mn)
            worst.append(mx)
    
    return np.array(best), np.array(worst)

def _euclidean(row1, row2):
    return (((row1 - row2)**2).sum())**(1/2)

# Main Function
def _topsis(original_df, weights, impacts):
    df = original_df.iloc[:, 1:]

    _normalize(df)
    _add_weights(df, weights)
    best, worst = _get_best_and_worst(df, impacts)

    s1 = []
    s2 = []
    for i in range(df.shape[0]):
        s1.append(_euclidean(np.array(df.iloc[i, :]), best))
        s2.append(_euclidean(np.array(df.iloc[i, :]), worst))

    df['s+'] = s1
    df['s-'] = s2
    df['p+'] = df['s-'] / (df['s-'] + df['s+'])

    df['rank'] = np.nan
    indices = np.argsort(df['p+'].values)[::-1]
    k = 1
    for i in indices:
        df.iloc[i, -1] = k
        k+=1

    original_df['Topsis Score'] = (df['p+']*100).round(2)
    original_df['Rank'] = df['rank'].astype(int)


def topsis(input_file, weights, impacts, output_file, want_roll=True):
    """
    Expects :-
    input_file -> "Excel/Csv" file path
    weights -> Comma seperated integers
    impacts -> Comma seperated +/- impacts
    output_file -> output csv file path"
    
    want_roll -> Set False if you don't want to create copy of input data.
    Preffered is False but set to true coz college assignment xD

    Outputs:-
    Creates a csv file on "output_file" path containing score and Ranks

    NOTE: No Validation is done in this function
    """
    # PreProcessing
    weights = [int(w) for w in weights.split(',')]
    impacts = impacts.split(',')

    # Excel to DataFrame Conversion
    if str(input_file).endswith('.csv'):
        original_df = pd.read_csv(input_file)
    else:
        original_df = pd.read_excel(input_file)

    # Validation
    data_validations(original_df, weights, impacts)

    # Main Work
    if want_roll:
        original_df.to_csv(f'101917014-data.csv', index=False)
    _topsis(original_df, weights, impacts)
    original_df.to_csv(output_file, index=False)
