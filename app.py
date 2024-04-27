import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
import numpy as np
from joblib import dump

data = pd.read_csv('cleaned_data.csv')

data['right_ascension'] = pd.to_numeric(data['right_ascension'], errors='coerce')
data['declination'] = pd.to_numeric(data['declination'], errors='coerce')

features = data[['right_ascension', 'declination']]
target = data['constellation']

scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

X_train, X_test, y_train, y_test = train_test_split(features_scaled, target, test_size=0.2, random_state=1432)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

knn = KNeighborsClassifier(n_neighbors=15)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")

dump(scaler, 'scaler.joblib')  
dump(knn, 'knn_model.joblib')
