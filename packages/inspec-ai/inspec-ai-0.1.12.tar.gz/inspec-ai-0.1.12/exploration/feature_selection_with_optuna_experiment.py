"""
Feature selection with optuna experiment
========================================

This script uses the bayesian optimizer optuna to select features in a Monte Carlo simulation and
compares its selection with a lasso regularisation (l1 penalized regression). The simulation generates
a N by 6 X matrix of random numbers from a N(0, 1) distribution. The y vector is given by
Xcol1 + 2*Xcol2 + 10*Xcol3 + Xcol4**2 + N(0, 1) gaussian noise.

It is found that the bayesian optimizer can identify useful variables and reject useless variables.

However, the base implementation of Optuna is not efficient for optimizing categorical
variables, as it often repeats trials with the same categorical inputs. The computing cost grew quickly for
bigger datasets (>10k observations), since a baseline model is trained at each iteration.

You will need a few packages to run the experiment (numpy, optuna, sklearn) and decently recent python version.
"""


import numpy as np
import optuna
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error


def bayesian_feature_selection(x, y):
    def objective(trial):
        columns_selection = [trial.suggest_categorical(i, [True, False]) for i in range(x.shape[1])]
        useless_column = np.zeros((len(x), 1))  # to avoid empty X

        _x = np.column_stack([
            x[:, columns_selection],
            useless_column
        ])

        baseline_model = RandomForestRegressor()
        baseline_model.fit(_x, y.ravel())
        pred = baseline_model.predict(_x)

        return mean_squared_error(y, pred, squared=False)

    study = optuna.create_study()

    study.optimize(objective, n_trials=100)

    return study.best_params, optuna.importance.get_param_importances(study)


def lasso_selection(x, y):
    model = Lasso(alpha=0.3)
    model.fit(x, y)

    sum_of_coefficients = np.sum(np.abs(model.coef_))

    selected_features = {column_number: coefficient != 0 for column_number, coefficient in enumerate(model.coef_)}
    features_importance = {column_number: abs(coefficient)/sum_of_coefficients for column_number, coefficient in enumerate(model.coef_)}

    return selected_features, features_importance


def monte_carlo(sample_size=1000):
    important_feature_1 = np.random.normal(size=(sample_size, 1))
    important_feature_2 = np.random.normal(size=(sample_size, 1))
    important_feature_3 = np.random.normal(size=(sample_size, 1))
    important_feature_4 = np.random.normal(size=(sample_size, 1))
    unimportant_feature_1 = np.random.normal(size=(sample_size, 1))
    unimportant_feature_2 = np.random.normal(size=(sample_size, 1))

    x = np.column_stack([important_feature_1, important_feature_2, important_feature_3, important_feature_4, unimportant_feature_1, unimportant_feature_2])
    y = important_feature_1 + 2 * important_feature_2 + 10 * important_feature_3 + important_feature_4 ** 2 + np.random.normal(size=(sample_size, 1))

    return x, y


def run_experiment():
    np.random.seed(42)

    x, y = monte_carlo()
    lasso_best_features, lasso_features_importance = lasso_selection(x, y)
    bayes_best_features, bayes_features_importance = bayesian_feature_selection(x, y)

    print("Lasso features: " + str(lasso_best_features))
    print("Bayes features: " + str(bayes_best_features))
    print("Lasso importance: " + str(lasso_features_importance))
    print("Bayes importance: " + str(bayes_features_importance))


if __name__ == "__main__":
    run_experiment()
