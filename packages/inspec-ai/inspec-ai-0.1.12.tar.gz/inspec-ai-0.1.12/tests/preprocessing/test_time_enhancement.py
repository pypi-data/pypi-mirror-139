from datetime import datetime

import pandas as pd
import pytest

from inspec_ai.preprocessing.time_enhancement import (
    get_predictive_time_features,
    time_enhancement,
    DATES_NOT_A_PD_SERIES_ERROR,
    DATES_NOT_A_DATETIME_DTYPE_ERROR,
    INVALID_PERIODICITY_ERROR,
    CUSTOM_DATES_NOT_DICT_ERROR,
    CUSTOM_DATES_VALUE_INVALID_TYPE_ERROR,
    CUSTOM_DATES_LIST_VALUE_WITH_INVALID_ELEMENTS_ERROR,
)


def test_get_predictive_time_features__10_years_time_series__returns_correct_columns():
    dates = pd.Series(pd.date_range("2020-01-01", "2030-12-31"))
    time_features = time_enhancement(dates)
    y = time_features["sine"].values + time_features["Monday"] + time_features["Friday"]

    predictive_time_features = get_predictive_time_features(dates, y)

    assert set(predictive_time_features.columns) == {"Monday", "Friday", "sine"}


def test_get_predictive_time_features__2_years_panel__returns_correct_columns():
    n_products = 5
    single_product_dates = pd.Series(pd.date_range("2020-01-01", "2022-12-31"))

    dates = pd.concat([single_product_dates] * n_products).reset_index(drop=True)
    time_features = time_enhancement(dates)
    y = time_features["sine"].values + time_features["Monday"] + time_features["Friday"]

    predictive_time_features = get_predictive_time_features(dates, y)

    assert set(predictive_time_features.columns) == {"Monday", "Friday", "sine"}


def test__time_enhancement__dates_not_pd_series__raises_error():
    dates = list()

    with pytest.raises(ValueError) as e:
        time_enhancement(dates)

    assert str(e.value) == DATES_NOT_A_PD_SERIES_ERROR.format(input_type="<class 'list'>")


def test__time_enhancement__dates_dtype_not_pd_datetime__raises_error():
    dates = pd.Series(["1", "2", "3"])

    with pytest.raises(ValueError) as e:
        time_enhancement(dates)

    assert str(e.value) == DATES_NOT_A_DATETIME_DTYPE_ERROR.format(input_dtype="object")


def test__time_enhancement__invalid_periodicity__raises_error():
    dates = pd.Series([datetime.strptime("2020-01-01", "%Y-%m-%d")])
    periodicity = "Not a valid periodicity"

    with pytest.raises(ValueError) as e:
        time_enhancement(dates, periodicity)

    assert str(e.value) == INVALID_PERIODICITY_ERROR.format(periodicity=periodicity)


def test__time_enhancement__custom_dates_not_dict__raises_error():
    dates = pd.Series([datetime.strptime("2020-01-01", "%Y-%m-%d")])
    custom_dates = [1, 2]

    with pytest.raises(ValueError) as e:
        time_enhancement(dates, custom_dates=custom_dates)

    assert str(e.value) == CUSTOM_DATES_NOT_DICT_ERROR.format(input_type="<class 'list'>")


def test__time_enhancement__custom_dates_value_invalid_type__raises_error():
    dates = pd.Series([datetime.strptime("2020-01-01", "%Y-%m-%d")])
    custom_dates = {"custom date": 1}

    with pytest.raises(ValueError) as e:
        time_enhancement(dates, custom_dates=custom_dates)

    assert str(e.value) == CUSTOM_DATES_VALUE_INVALID_TYPE_ERROR.format(custom_dates_value_type="<class 'int'>")


def test__time_enhancement__custom_dates_value_list_with_invalid_element_type__raises_error():
    dates = pd.Series([datetime.strptime("2020-01-01", "%Y-%m-%d")])
    custom_dates = {"custom date": [1]}

    with pytest.raises(ValueError) as e:
        time_enhancement(dates, custom_dates=custom_dates)

    assert str(e.value) == CUSTOM_DATES_LIST_VALUE_WITH_INVALID_ELEMENTS_ERROR.format(custom_dates_list_value_type="<class 'int'>")


def test__time_enhancement__monthly_data__correct_month_dummy_variables():
    dates = pd.Series(
        [
            datetime.strptime("2020-01-01", "%Y-%m-%d"),
            datetime.strptime("2020-02-13", "%Y-%m-%d"),
            datetime.strptime("2022-11-27", "%Y-%m-%d"),
            datetime.strptime("2023-11-23", "%Y-%m-%d"),
        ]
    )

    time_features = time_enhancement(dates, "M")

    assert (time_features["January"] == [1, 0, 0, 0]).all()
    assert (time_features["February"] == [0, 1, 0, 0]).all()
    assert (time_features["November"] == [0, 0, 1, 1]).all()


def test__time_enhancement__daily_data__correct_week_dummy_variables():

    dates = pd.Series(
        [
            datetime.strptime("2020-01-01", "%Y-%m-%d"),
            datetime.strptime("2020-02-13", "%Y-%m-%d"),
            datetime.strptime("2022-11-27", "%Y-%m-%d"),
            datetime.strptime("2023-11-23", "%Y-%m-%d"),
        ]
    )

    time_features = time_enhancement(dates, "D")

    assert (time_features["Week_1"] == [1, 0, 0, 0]).all()
    assert (time_features["Week_7"] == [0, 1, 0, 0]).all()
    assert (time_features["Week_47"] == [0, 0, 1, 1]).all()


def test__time_enhancement__daily_data__correct_day_of_week_dummies():
    dates = pd.Series(
        [
            datetime.strptime("2022-01-24", "%Y-%m-%d"),
            datetime.strptime("2022-01-25", "%Y-%m-%d"),
            datetime.strptime("2022-01-26", "%Y-%m-%d"),
            datetime.strptime("2022-01-27", "%Y-%m-%d"),
            datetime.strptime("2022-01-28", "%Y-%m-%d"),
            datetime.strptime("2022-01-29", "%Y-%m-%d"),
            datetime.strptime("2022-01-30", "%Y-%m-%d"),
        ]
    )

    time_features = time_enhancement(dates, "D")

    assert (time_features["Monday"] == [1, 0, 0, 0, 0, 0, 0]).all()
    assert (time_features["Tuesday"] == [0, 1, 0, 0, 0, 0, 0]).all()
    assert (time_features["Wednesday"] == [0, 0, 1, 0, 0, 0, 0]).all()
    assert (time_features["Thursday"] == [0, 0, 0, 1, 0, 0, 0]).all()
    assert (time_features["Friday"] == [0, 0, 0, 0, 1, 0, 0]).all()
    assert (time_features["Saturday"] == [0, 0, 0, 0, 0, 1, 0]).all()
    assert (time_features["Sunday"] == [0, 0, 0, 0, 0, 0, 1]).all()


def test__time_enhancement__daily_data__correct_qc_holiday_dummies():
    dates = pd.Series(
        [
            datetime.strptime("2020-01-01", "%Y-%m-%d"),
            datetime.strptime("2020-06-24", "%Y-%m-%d"),
            datetime.strptime("2022-06-24", "%Y-%m-%d"),
            datetime.strptime("2023-12-26", "%Y-%m-%d"),
            datetime.strptime("2001-12-15", "%Y-%m-%d"),
            datetime.strptime("2020-12-28", "%Y-%m-%d"),
        ]
    )

    time_features = time_enhancement(dates, "D")

    assert (time_features["holiday_New Year's Day"] == [1, 0, 0, 0, 0, 0]).all()
    assert (time_features["holiday_St. Jean Baptiste Day"] == [0, 1, 1, 0, 0, 0]).all()
    assert (time_features["holiday_Boxing Day"] == [0, 0, 0, 1, 0, 1]).all()


def test__time_enhancement__daily_data__correct_trigonometric_features():
    dates = pd.Series(
        [
            datetime.strptime("2021-01-01", "%Y-%m-%d"),
            datetime.strptime("2021-03-31", "%Y-%m-%d"),
            datetime.strptime("2021-07-02", "%Y-%m-%d"),
            datetime.strptime("2021-09-30", "%Y-%m-%d"),
            datetime.strptime("2021-12-31", "%Y-%m-%d"),
        ]
    )

    expected_sine = pd.Series([0, 1, 0, -1, 0])
    expected_cosine = pd.Series([1, 0, -1, 0, 1])

    time_features = time_enhancement(dates, "D")

    assert ((time_features["sine"] - expected_sine).abs() < 0.025).all()
    assert ((time_features["cosine"] - expected_cosine).abs() < 0.025).all()


def test__time_enhancement__daily_data_custom_dates__correct_custom_dates():
    custom_dates = {
        "Superbowl": [
            "2017-02-05",
            "2018-02-04",
            "2019-02-03",
            "2020-02-02",
            "2021-02-07",
            "2022-02-13",
            "2023-02-12",
            "2024-02-11",
            "2025-02-09",
            "2026-02-01",
            "2027-02-07",
            "2028-02-06",
            "2029-02-04",
            datetime.strptime("2030-02-03", "%Y-%m-%d"),
        ],
        "A very special day": "2069-04-20",
        "Another very special day": datetime.strptime("2012-12-12", "%Y-%m-%d"),
    }

    dates = pd.Series(
        [
            datetime.strptime("2017-02-05", "%Y-%m-%d"),
            datetime.strptime("2030-02-03", "%Y-%m-%d"),
            datetime.strptime("2022-06-24", "%Y-%m-%d"),
            datetime.strptime("2069-04-20", "%Y-%m-%d"),
            datetime.strptime("2012-12-12", "%Y-%m-%d"),
        ]
    )

    time_features = time_enhancement(dates, "D", custom_dates)

    assert (time_features["Superbowl"] == [1, 1, 0, 0, 0]).all()
    assert (time_features["A very special day"] == [0, 0, 0, 1, 0]).all()
    assert (time_features["Another very special day"] == [0, 0, 0, 0, 1]).all()


def test__time_enhancement__daily_date_custom_dates_not_same_hour__correct_custom_dates():
    custom_dates = {"A custom date": "2020-01-12"}

    dates = pd.Series(
        [
            datetime.strptime("2020-01-01", "%Y-%m-%d"),
            datetime.strptime("2020-01-12", "%Y-%m-%d"),
            datetime.strptime("2020-01-12 01:23:45", "%Y-%m-%d %H:%M:%S"),
        ]
    )

    time_features = time_enhancement(dates, "D", custom_dates)

    assert (time_features["A custom date"] == [0, 1, 1]).all()
