import pytest
import numpy as np
import pandas as pd

from inspec_ai.preprocessing.predictive_features import get_predictive_features


def test__get_predictive_features__when_single_columns_has_positive_coefficient__works():
    x_train = np.array(
        [
            [1, 3],
            [2, 1],
            [3, 4],
            [4, 1],
            [5, 5],
            [6, 9],
            [7, 2],
            [8, 6],
            [9, 5],
            [10, 3],
        ]
    )

    y_train = x_train[:, 0]

    optimal_features, coefficients = get_predictive_features(x_train, y_train)

    assert len(x_train) == len(optimal_features)
    assert 1 == optimal_features.shape[1]
    assert (np.reshape(x_train[:, 0], (10, 1)) == optimal_features).all()

    assert coefficients[0] > 0
    assert coefficients[1] == 0


def test__get_predictive_features__when_multiple_columns_have_positive_coefficient__works():
    x_train = np.array(
        [
            [1, 11, 3],
            [2, 12, 1],
            [3, 13, 4],
            [4, 14, 1],
            [5, 15, 5],
            [6, 16, 9],
            [7, 17, 2],
            [8, 18, 6],
            [9, 19, 5],
            [10, 20, 3],
        ]
    )

    y_train = x_train[:, 0] + x_train[:, 1]

    optimal_features, coefficients = get_predictive_features(x_train, y_train)

    assert len(x_train) == len(optimal_features)
    assert 2 == optimal_features.shape[1]
    assert (np.reshape(x_train[:, 0:2], (10, 2)) == optimal_features).all()

    assert coefficients[0] > 0
    assert coefficients[1] > 0
    assert coefficients[2] <= 0


def test__get_predictive_features__when_predictions_all_zeros__returns_empty():
    x_train = np.array(
        [
            [1, 3],
            [2, 1],
            [3, 4],
            [4, 1],
            [5, 5],
            [6, 9],
            [7, 2],
            [8, 6],
            [9, 5],
            [10, 3],
        ]
    )

    y_train = np.zeros(shape=(len(x_train),))

    optimal_features, coefficients = get_predictive_features(x_train, y_train)

    assert 0 == optimal_features.size
    assert all([coef == 0 for coef in coefficients.values()])


def test__get_predictive_features__when_pandas_dataframe__works():
    x_train = pd.DataFrame(
        [
            [1, 3],
            [2, 1],
            [3, 4],
            [4, 1],
            [5, 5],
            [6, 9],
            [7, 2],
            [8, 6],
            [9, 5],
            [10, 3],
        ],
        columns=["col1", "col2"],
    )

    y_train = x_train["col1"]

    optimal_features, coefficients = get_predictive_features(x_train, y_train)

    assert len(x_train) == len(optimal_features)
    assert 1 == optimal_features.shape[1]
    assert (x_train["col1"].values.reshape(-1, 1) == optimal_features.values).all()
    assert coefficients["col1"] > 0
    assert coefficients["col2"] == 0


def test__get_predictive_features__when_inputs_do_not_have_same_size__raises():
    x_train = np.array([[1, 3], [2, 1], [3, 4], [4, 1]])

    y_train = np.array([1, 2])

    with pytest.raises(ValueError) as e:
        _, _ = get_predictive_features(x_train, y_train)

    assert str(e.value) == "The provided inputs must contain the same number of elements: x_train and y_train."
