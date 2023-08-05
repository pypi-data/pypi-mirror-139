## Grouping similar string values in a categorical feature

### Overview

The class *CategoryCleaner* located at inspec/messy_categories/category_cleaner.py helps you identified and group similar values in a categorical feature.
For example, can help you spot typos.
Or values that represent the same thing in different data sources, but once all put together in the same column creates useless values.
Can identify and group examples similar to:
- "Montreal" and "Montréal"
- "Toronto Raptors" and "Raptors"
- "female" and "Femal"

### Usage

```python
import pandas as pd
from inspec_ai.preprocessing.category_cleaner import CategoryCleaner

df = pd.read_csv("./some-dataset.csv")

# If you already have a pandas_profiling report, you can pass it to the cleaner to accelerate execution
cleaner = CategoryCleaner(df)

clean_df = cleaner.get_cleaned_df()
```

Want to try this prototype but you don't have a dataset? You can generate a fake dataset by running `inspec_ai/_datasets/messy_categories.py` (should output in `.out/with_null_data_messy_categories.csv`) and use it in the previous script.