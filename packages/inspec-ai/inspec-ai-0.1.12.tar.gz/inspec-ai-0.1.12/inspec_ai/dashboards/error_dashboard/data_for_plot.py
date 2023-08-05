import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from inspec_ai._datasets.covid_variants import covid_variants


def get_default_dashboard_values():
    df = covid_variants()

    df = df.sort_values(["country", "variant", "date"]).reset_index(drop=True)
    df["lag_share_of_cases"] = df.groupby(["country", "variant"])["share_of_cases"].shift()

    y_test = df.dropna()["share_of_cases"]
    X_test = df.drop(columns="share_of_cases").dropna()

    model = RandomForestRegressor()
    model.fit(X_test["lag_share_of_cases"].values.reshape(-1, 1), y_test.values)

    pred = model.predict(X_test["lag_share_of_cases"].values.reshape(-1, 1))

    return X_test, y_test, pred


def get_covid_dataset_values():
    df = covid_variants()
    df = df.sort_values(["country", "variant", "date"]).reset_index(drop=True)
    df["lag_share_of_cases"] = df.groupby(["country", "variant"])["share_of_cases"].shift()

    y = df["share_of_cases"]
    X = df.drop(columns="share_of_cases").dropna()

    return X, y


def get_random_predictions(y_train: pd.DataFrame) -> pd.DataFrame:
    min = y_train.min()
    max = y_train.max()

    return np.random.randint(min, high=max, size=len(y_train))


def get_random_forest_regressor_predictions(X_train: pd.DataFrame, y_train: pd.DataFrame, X_test: pd.DataFrame) -> pd.DataFrame:
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    return pred
