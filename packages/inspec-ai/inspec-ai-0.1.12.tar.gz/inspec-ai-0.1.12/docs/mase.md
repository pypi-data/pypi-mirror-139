## Measuring the Mean Absolute Scaled Error (MASE)

### Overview

For more information on the MASE (Mean Absolute Scaled Error) and why it is important to measure it, please consult the following documentation page: 

https://moovai.atlassian.net/wiki/spaces/SNIT/pages/1239187457/Erreurs+de+mesure+en+s+ries+temporelles

### Usage

There are two ways to measure the MASE:

To measure the MASE between the test_y and the predictions made by the model based on the test_x, you can use the following function:

_mean_absolute_scaled_error(y_true, y_pred) -> float_

```python
import joblib
import pandas as pd
from inspec_ai.metrics.mase import mean_absolute_scaled_error

test_x = pd.read_csv('a_time_series.csv')
test_y = pd.read_csv('a_time_series_targets.csv')

model = joblib.load('model.joblib')

pred = model.predict(test_x)

# Note that test_y and pred must be sorted by time
mase = mean_absolute_scaled_error(test_y, pred)

print(mase) 

# Output:
# 5.4
```

To measure the MASE of a timeseries, you can use the following function:

_mase_by_series(y_true, y_pred, dimension=None, time=None) -> pd.Series_

```python
import joblib
import pandas as pd
from inspec_ai.metrics.mase import mase_by_series


test_x = pd.read_csv('multiple_time_series.csv')
test_y = pd.read_csv('multiple_time_series_targets.csv')

model = joblib.load('model.joblib')

pred = model.predict(test_x)

# Where dimension is a pandas series with product identifiers (ex.: IDs, country, bus line, user, etc.) in the string or number format.
# Where time is a pandas series
metrics = mase_by_series(test_y, pred, dimension = test_x['product'], time = test_x['date'])

print(metrics.iloc[0, :])

# Output:
# product      'langues de porc'
# mase         64.12
```