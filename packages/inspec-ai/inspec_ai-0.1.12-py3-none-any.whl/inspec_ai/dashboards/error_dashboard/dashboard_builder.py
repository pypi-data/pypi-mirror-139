import warnings
from copy import deepcopy
from typing import Dict, List, Union

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html
from dash_extensions.enrich import DashProxy, Input, MultiplexerTransform, Output
from pandas.api.types import is_datetime64_any_dtype as is_datetime
from pandas.api.types import is_float_dtype as is_float

from inspec_ai.dashboards.error_dashboard.data_for_plot import get_default_dashboard_values
from inspec_ai.metrics.mase import mase_by_series

TOP_ERROR_COUNT = 5

FILTER_ID_PREFIX = "filter-"

app = DashProxy(prevent_initial_callbacks=True, transforms=[MultiplexerTransform()])

current_filters: Dict[str, Union[str, List, Dict]] = {}


def _format_filter_component_id(column_value: str) -> str:
    return FILTER_ID_PREFIX + column_value


def _get_column_id_from_filter_id(column_value: str) -> str:
    return column_value.replace(FILTER_ID_PREFIX, "")


def _handle_filter_updates(
    X_test: pd.DataFrame,
    y_test: Union[pd.DataFrame, pd.Series],
    errors: Union[pd.DataFrame, pd.Series],
) -> go.Figure:
    global current_filters

    y_test_copy = deepcopy(y_test)
    errors_copy = deepcopy(errors)

    for filter_key, filter_value in current_filters.items():
        if filter_value:
            if isinstance(filter_value, dict) and is_datetime(filter_value["type"]):
                start_date = filter_value["start_date"]
                end_date = filter_value["end_date"]

                y_test_copy = y_test_copy[X_test[filter_key] >= start_date]
                y_test_copy = y_test_copy[X_test[filter_key] <= end_date]
                errors_copy = errors_copy[X_test[filter_key] >= start_date]
                errors_copy = errors_copy[X_test[filter_key] <= end_date]

            elif isinstance(filter_value, list) and len(filter_value) == 2:
                min = filter_value[0]
                max = filter_value[1]

                y_test_copy = y_test_copy[X_test[filter_key] >= min]
                y_test_copy = y_test_copy[X_test[filter_key] <= max]
                errors_copy = errors_copy[X_test[filter_key] >= min]
                errors_copy = errors_copy[X_test[filter_key] <= max]

            else:
                y_test_copy = y_test_copy[X_test[filter_key] == filter_value]
                errors_copy = errors_copy[X_test[filter_key] == filter_value]

    df_tmp = pd.DataFrame({"y": y_test_copy, "residuals": errors_copy})

    error_fig = px.scatter(df_tmp, x="y", y="residuals")
    error_fig.add_hline(y=0, line_dash="dot")

    return error_fig


def _generate_main_filters(
    X_test: pd.DataFrame,
    y_test: Union[pd.DataFrame, pd.Series],
    errors: Union[pd.DataFrame, pd.Series],
    dimension: Union[pd.DataFrame, pd.Series],
    time: Union[pd.DataFrame, pd.Series],
) -> List:
    components = []

    time_min = time.min()
    time_max = time.max()

    components.append(
        dcc.DatePickerRange(
            id="time-filter",
            min_date_allowed=time_min,
            max_date_allowed=time_max,
            start_date=time_min,
            end_date=time_max,
        )
    )

    @app.callback(
        Output(component_id="main-graph", component_property="figure"),
        Input("time-filter", "start_date"),
        Input("time-filter", "end_date"),
    )
    def dynamic_date_callback(start_date, end_date):
        global current_filters
        current_filters[time.name] = {
            "type": time.dtype,
            "start_date": start_date,
            "end_date": end_date,
        }

        return _handle_filter_updates(X_test, y_test, errors)

    components.append(
        dcc.Dropdown(
            id="dimension-filter",
            style={"min-width": "10%"},
            options=dimension.unique(),
            placeholder=dimension.name,
            value=None,
            clearable=True,
            searchable=True,
        )
    )

    @app.callback(
        Output(component_id="main-graph", component_property="figure"),
        Input(component_id="dimension-filter", component_property="value"),
    )
    def dynamic_callback(value):
        global current_filters
        current_filters[dimension.name] = value

        return _handle_filter_updates(X_test, y_test, errors)

    return components


def _generate_filter_components(
    X_test: pd.DataFrame,
    y_test: Union[pd.DataFrame, pd.Series],
    errors: Union[pd.DataFrame, pd.Series],
    dimension: Union[pd.DataFrame, pd.Series],
    time: Union[pd.DataFrame, pd.Series],
) -> List:
    components = []

    possible_filters = X_test.drop(labels=[dimension.name, time.name], axis=1)

    for column in possible_filters.columns:
        component_id = FILTER_ID_PREFIX + column

        if is_float(X_test[column].dtype):
            float_min = X_test[column].min()
            float_max = X_test[column].max()

            components.append(html.P(children=column))
            components.append(
                dcc.RangeSlider(
                    float_min,
                    float_max,
                    id=component_id,
                    value=[float_min, float_max],
                    tooltip={
                        "placement": "bottom",
                        "always_visible": True,
                    },
                ),
            )

            @app.callback(
                Output(component_id="main-graph", component_property="figure"),
                [
                    Input(component_id=component_id, component_property="value"),
                    Input(component_id=component_id, component_property="id"),
                ],
            )
            def dynamic_callback(value, id):
                global current_filters
                column_name = _get_column_id_from_filter_id(id)
                current_filters[column_name] = value

                return _handle_filter_updates(X_test, y_test, errors)

        else:
            components.append(html.P(children=column))
            components.append(
                dcc.Dropdown(
                    id=component_id,
                    options=X_test[column].unique(),
                    placeholder=column,
                    value=None,
                    clearable=True,
                    searchable=True,
                )
            )

            @app.callback(
                Output(component_id="main-graph", component_property="figure"),
                [
                    Input(component_id=component_id, component_property="value"),
                    Input(component_id=component_id, component_property="id"),
                ],
            )
            def dynamic_callback(value, id):
                global current_filters
                column_name = _get_column_id_from_filter_id(id)
                current_filters[column_name] = value

                return _handle_filter_updates(X_test, y_test, errors)

    return components


def _get_top_error_components(
    X_test: pd.DataFrame,
    y_test: Union[pd.DataFrame, pd.Series],
    predictions: Union[pd.DataFrame, pd.Series, np.ndarray],
    dimension: Union[pd.DataFrame, pd.Series],
    time: Union[pd.DataFrame, pd.Series],
) -> List:
    components = []

    mase = mase_by_series(y_test, predictions, dimension, time)

    for i in range(0, min(TOP_ERROR_COUNT, len(predictions))):
        graph_id = "top_error_graph_" + str(i)
        mase_index = mase.index[i]
        mase_value = mase[i]

        top_y_test = y_test[dimension == mase_index]
        top_y_predictions = predictions[dimension == mase_index]

        top_y_error = top_y_test - top_y_predictions

        df_top_error = pd.DataFrame({"y": top_y_test, "residuals": top_y_error})

        top_error_fig = px.scatter(df_top_error, x="y", y="residuals")
        top_error_fig.add_hline(y=0, line_dash="dot")

        components.append(
            html.Div(
                style={"display": "flex", "flex-direction": "column", "width": str(100 / TOP_ERROR_COUNT) + "%"},
                children=[
                    html.Div(style={"text-align": "center"}, children=str(mase_index)),
                    dcc.Graph(id=graph_id, figure=top_error_fig),
                    html.Div(style={"text-align": "center"}, children="MASE: " + str("%.2f" % mase_value)),
                ],
            )
        )

    return components


def build_dashboard_app(
    X_test: pd.DataFrame = None,
    y_test: Union[pd.DataFrame, pd.Series] = None,
    predictions: Union[pd.DataFrame, pd.Series, np.ndarray] = None,
    dimension: Union[pd.DataFrame, pd.Series] = None,
    time: Union[pd.DataFrame, pd.Series] = None,
) -> DashProxy:
    # Check all values are None
    if X_test is None and y_test is None and predictions is None and dimension is None and time is None:
        warnings.warn("Dashboard invoked without any values: using default values.")

        X_test, y_test, predictions = get_default_dashboard_values()
        dimension = X_test["variant"]
        time = X_test["date"]

    # Check if missing inputs
    elif X_test is None or y_test is None or predictions is None or dimension is None or time is None:
        raise ValueError("Dashboard cannot be invoked: missing inputs.")

    # Check if all pandas and not empty
    elif (
        isinstance(X_test, pd.DataFrame)
        and isinstance(y_test, (pd.DataFrame, pd.Series))
        and isinstance(predictions, (pd.DataFrame, pd.Series, np.ndarray))
        and isinstance(dimension, (pd.DataFrame, pd.Series))
        and isinstance(time, (pd.DataFrame, pd.Series))
    ):
        if len(X_test) == 0 and len(y_test) == 0 and len(predictions) == 0 and len(dimension) == 0 and len(time) == 0:
            warnings.warn("Dashboard invoked with all empty values: using default values.")

            X_test, y_test, predictions = get_default_dashboard_values()
            dimension = X_test["variant"]
            time = X_test["date"]

        elif len(X_test) == 0 or len(y_test) == 0 or len(predictions) == 0 or len(dimension) == 0 or len(time) == 0:
            raise ValueError("Dashboard cannot be build: some inputs are empty datasets.")

    else:
        raise ValueError("Unsupported input types. Please ensure that you providing Pandas Dataframes or Pandas Series.")

    errors = y_test - predictions

    df = pd.DataFrame({"y": y_test, "residuals": errors})

    main_error_fig = px.scatter(df, x="y", y="residuals")
    main_error_fig.add_hline(y=0, line_dash="dot")

    filter_components = _generate_filter_components(X_test, y_test, errors, dimension, time)

    top_error_components = _get_top_error_components(X_test, y_test, predictions, dimension, time)

    app.layout = html.Div(
        children=[
            html.H1(id="title-id", children="Error Exploration Dashboard"),
            html.Div(
                style={"display": "flex", "flex-direction": "row"},
                children=[
                    html.Div(
                        style={"width": "10%"},
                        children=[
                            html.H4(children="Filters"),
                            html.Div(
                                style={"width": "100%"},
                                children=filter_components,
                            ),
                        ],
                    ),
                    html.Div(
                        style={"display": "flex", "flex-direction": "column", "width": "90%"},
                        children=[
                            html.H2(
                                style={"text-align": "center"},
                                children=y_test.name,
                            ),
                            html.Div(
                                style={
                                    "display": "flex",
                                    "flex-direction": "row",
                                    "align-items": "center",
                                    "justify-content": "space-evenly",
                                },
                                children=_generate_main_filters(X_test, y_test, errors, dimension, time),
                            ),
                            dcc.Graph(id="main-graph", figure=main_error_fig),
                            html.H3(
                                style={"text-align": "center"},
                                children="Top Errors (dimension: " + str(dimension.name) + ")",
                            ),
                            html.Div(
                                style={"display": "flex", "flex-direction": "row"},
                                children=top_error_components,
                            ),
                        ],
                    ),
                ],
            ),
        ]
    )

    return app
