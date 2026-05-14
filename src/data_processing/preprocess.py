def preprocess_data(df):
    df = df.copy()
    df.drop_duplicates(inplace=True)
    df.fillna(0, inplace=True)
    return df