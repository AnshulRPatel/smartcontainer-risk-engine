def winsorize_columns(df, cols, lower=0.01, upper=0.99):

    for col in cols:

        low = df[col].quantile(lower)
        high = df[col].quantile(upper)

        df[col] = df[col].clip(low, high)

    return df