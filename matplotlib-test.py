import matplotlib
import importlib
# matplotlib.use('agg')

# matplotlib = importlib.reload(matplotlib)
# matplotlib.use("Qt5Agg")
matplotlib.rcParams['backend'] = 'TkAgg'
# matplotlib.rcParams['backend'] = 'Qt5Agg'
# matplotlib = importlib.reload(matplotlib)
import matplotlib.pyplot as plt
print(matplotlib.rcParams['backend'])
print(matplotlib.get_backend())
# print(plt.get_backend())