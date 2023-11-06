# import libraries
import requests
import random
import pandas as pd
import time
import pandas_gbq
import numpy as np
import re

def remove_index(string):
    # Remove extra commas
    string = re.sub(r",(?:\s+|,)+", " ", string)

    # Remove "index" or "index,"
    if re.search(r"\bindex\b", string):
        string = re.sub(r"\bindex\b", "", string)

    # Remove trailing comma
    if string.endswith(","):
        string = string[:-1]

    # Replace commas with spaces
    string = string.replace(",", " ")

    return string

def getMarketData(market):

    # print(f"Testing Market: {market}")
    var = "NA"
    indicators = pd.DataFrame(requests.get("https://us-central1-industrial-demand.cloudfunctions.net/multivariate-correlation", {"name": market, "var": var}).json())
    indicators = indicators.rename(columns={'NA': 'NetAbsorptionSF'})

    _selected_columns = []
    selected_columns = (indicators.columns)
    for col in selected_columns:
        if col == "index":
            print("")
        elif col == "MarketCapRate":
            col = "MarketCapRates"
            _selected_columns.append(col)
        else:
            _selected_columns.append(col)

    query = ", ".join(_selected_columns)

    sql_query = f"SELECT {query}, MarketName FROM `industrial-demand.source.cushman_Q3`;"

    project_id = "industrial-demand"
    df = pandas_gbq.read_gbq(sql_query, project_id=project_id)
    df = df.loc[df['MarketName'] == market].reset_index(drop=True)

    date = df["date"].tolist()

    df = df.drop("date", axis=1)
    df = df.drop("MarketName", axis=1)

    cols = [col for col in df.columns]
    for col in cols:
        try:
            if df[col].dtype == np.float64:
                df[col].fillna(df[col].mean(), inplace=True)
            else:
                df[col].replace("<NA>", "", inplace=True)
                df[col] = df[col].str.strip()
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                for i in range(len(df[col])):
                    df.loc[i, col] = np.float64(df.loc[i, col])

        except:
            df.drop(col, axis=1)

    min_values = df.min(axis=0)
    max_values = df.max(axis=0)

    for col in df.columns:
        df[col] = (df[col] - min_values[col]) / (max_values[col] - min_values[col])

    df["date"] = date
    return(df)

# test = "Denver - CO"
# df = getMarketData(test)
# print(df)