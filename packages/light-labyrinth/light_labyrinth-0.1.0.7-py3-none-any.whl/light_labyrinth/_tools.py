from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
import numpy as np

class _MinMaxLabyrinthEncoder:
    def __init__(self):
        self._encoder = MinMaxScaler()

    def fit(self, X):
        return self._encoder.fit(X)

    def transform(self, X):
        scaled = self._encoder.transform(X)
        return np.hstack((scaled, 1 - scaled))

    def fit_transform(self, X):
        scaled = self._encoder.fit_transform(X)
        return np.hstack((scaled, 1 - scaled))

    def inverse_transform(self, X):
        return self._encoder.inverse_transform(X[:, 0].reshape(-1,1))


class _SmartOneHotEncoder:
    def __init__(self):
        self._encoder = OneHotEncoder()

    def fit(self, X):
        self._org_shape = [-1, *X.shape[1:]]
        return self._encoder.fit(X.reshape((-1, 1)))

    def transform(self, X):
        return self._encoder.transform(X.reshape((-1, 1))).todense()

    def fit_transform(self, X):
        self._org_shape = [-1, *X.shape[1:]]
        return self._encoder.fit_transform(X.reshape((-1, 1))).todense()

    def inverse_transform(self, X):
        return self._encoder.inverse_transform(X).reshape(self._org_shape)

    def get_classes(self):
        return self._encoder.categories_[0]


class _MultioutputScaler:
    def __init__(self, epsilon=1e-9):
        self.epsilon = epsilon

    def fit(self, X):
        self._encoder = MinMaxScaler((0, 1/X.shape[1]))
        return self._encoder.fit(X)

    def transform(self, X):
        transformed = self._encoder.transform(X)
        self._org_shape = X.shape
        rest = 1/X.shape[1] - transformed
        n_columns = transformed.shape[1]
        column_order = sum([[i, i + n_columns] for i in range(n_columns)], [])
        prepared = np.hstack((transformed, rest))[:, column_order]
        return prepared

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)

    def inverse_transform(self, X):
        denominator = X[:, 0::2] + X[:, 1::2]
        zero_indices = denominator == 0
        denominator[zero_indices] = 1
        nominator = X[:, 0::2]
        nominator[zero_indices] = 0.5
        unprepared = nominator / denominator
        unprepared /= X.shape[1] / 2
        untrasformed = self._encoder.inverse_transform(unprepared)
        return untrasformed


class _MultilabelScaler:
    def __init__(self):
        self._encoder = _MultioutputScaler()

    def fit(self, X):
        return self._encoder.fit(X)

    def transform(self, X):
        return self._encoder.transform(X)

    def fit_transform(self, X):
        return self._encoder.fit_transform(X)

    def inverse_transform(self, X):
        return self._encoder.inverse_transform(X)

    def get_classes(self):
        return np.arange(self._encoder._org_shape[1])