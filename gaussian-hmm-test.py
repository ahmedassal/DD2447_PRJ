import numpy as np
from hmmlearn import hmm
from sklearn.externals import joblib

np.random.seed(42)

model = hmm.GaussianHMM(n_components=3, covariance_type="full")
model.startprob_ = np.array([0.6, 0.3, 0.1])
model.transmat_ = np.array([[0.7, 0.2, 0.1], \
                            [0.3, 0.5, 0.2], \
                            [0.3, 0.3, 0.4]])
model.means_ = np.array([[0.0, 0.0], [3.0, -3.0], [5.0, 10.0]])
model.covars_ = np.tile(np.identity(2), (3, 1, 1))
X, Z = model.sample(100)
print(X)
print(Z)

model.fit(X)
Z2 = model.predict(X)
print(Z2)
print(model.monitor_)
print(model.monitor_.converged)

joblib.dump(model, "testhmm-model.pkl")
joblib.load("testhmm-model.pkl")