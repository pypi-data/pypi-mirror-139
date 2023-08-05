## Error Dashboard

### Overview

The Error Dashboard is built using Plotly Dash and allows you to naviguate through your errors and see your highest errors by dimensions.

### Usage

You can build the dashboard with demo data using the following script:

```python
from inspec_ai.dashboards.error_dashboard import build_dashboard_app

app = build_dashboard_app()

app.run_server()
```

You can also build build the databoard with your own data:


```python
from inspec_ai.dashboards.error_dashboard import build_dashboard_app
from inspec_ai.dashboards.error_dashboard.data_for_plot import get_default_dashboard_values

X_test, y_test, predictions = get_default_dashboard_values()
dimension = X_test["variant"]
time = X_test["date"]

app = build_dashboard_app(X_test, y_test, predictions, dimension, time)

app.run_server()
```