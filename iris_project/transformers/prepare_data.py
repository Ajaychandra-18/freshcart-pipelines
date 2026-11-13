from sklearn.model_selection import train_test_split

def transform(df, *args, **kwargs):
    _, test = train_test_split(df, test_size=0.3, random_state=42)
    df = df.copy()
    df["split"] = "train"
    df.loc[test.index, "split"] = "test"
    return df
