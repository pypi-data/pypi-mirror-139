"""
Experimenting with the darts package
====================================

Tried the darts package for univariate time series predictions. It is found that it is quite simple
to quickly generate predictions, with both classical and deep learning models.
"""

import darts
from darts.models import ExponentialSmoothing, NBEATSModel
from darts.metrics import mae
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

season = np.sin(np.random.randint(0, 100, 100))
trend = np.arange(0, 100)/10
gauss_noise = np.random.normal(0, 3, 100)

series = season + trend + gauss_noise
ts = darts.TimeSeries.from_values(series)

train, test = ts[:-30], ts[-30:]

model = ExponentialSmoothing()
model.fit(train)
prediction = model.predict(len(test), num_samples=1000)

model2 = NBEATSModel(24, 12)
model2.fit(train)
prediction2 = model2.predict(len(test), num_samples=1000)

ts.plot(label='series')
prediction.plot(label='exp smoothing forecast', low_quantile=0.05, high_quantile=0.95)
prediction2.plot(label='nbeats forecast', low_quantile=0.05, high_quantile=0.95)

plt.show()
plt.clf()

mae1 = mae(test, prediction)
mae2 = mae(test, prediction2)

print(f"exp smoothing mae: {round(mae1, 4)}")
print(f"nbeats mae: {round(mae2, 4)}")
