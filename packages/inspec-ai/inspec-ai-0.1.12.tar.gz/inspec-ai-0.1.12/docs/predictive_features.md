## Identifying the predictive features of a dataset

### Overview

This prototype will identity the features with the most predictive power. We use a Lasso model and observe the predictive power of each feature.

### Usage

```python
import pandas as pd
from inspec_ai.preprocessing.predictive_features import get_predictive_features

train_x = pd.read_csv('a_time_series.csv')
train_y = pd.read_csv('a_time_series_targets.csv')

# You can also pass the alpha that will be used when establishing the predictive power of each feature.
predictive_features, coefficients = get_predictive_features(train_x, train_y)
```