from merf.utils import MERFDataGenerator
from merf.merf import MERF
from merf.viz import plot_merf_training_stats
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns

import copy
# Train.csv has the Field_IDs needed to find the npy files
x = pd.read_csv('Train.csv')
print(x)
x.head()

X3 = copy.deepcopy(x)  
for i in labels:
    X3[i] = (X3[i])**(1./10.)
for i in labels:
    print(i)
    print(skew(X3[i]))

xk = copy.deepcopy(X3)
#del xk['Field_ID']


xk['cluster'] = X3['labels']

xmixed, ymixed, clusters  = xk[xk.columns[:-1]], y, xk['cluster']

X_train, X_test, y_train, y_test, cluster_train, cluster_test = train_test_split(xmixed, ymixed, clusters, test_size=0.15)
Z_train = np.ones((len(X_train), 1))
Z_test = np.ones((len(X_test), 1))

# fit by setting best parameters and Evaluate model
mrf = MERF(max_iterations=150)
mrf.fit(X_train, Z_train, y_train, cluster_train)

#y_pred = mrf.predict(X_test, Z_test, cluster_test)

#print('Score:', mean_squared_error(y_test, y_pred, squared=False))
# make predictions for test data

mrf = MERF(max_iterations=150)
mrf.fit(X_train, Z_train, cluster_train, y_train, X_test, Z_test, cluster_test, y_test)

plot_merf_training_stats(mrf, num_clusters_to_plot=150)

y_pred = mrf.predict(X_test, Z_test, cluster_test)

print('Score:', mean_squared_error(y_test, y_pred, squared=False))
# make predictions for test data
