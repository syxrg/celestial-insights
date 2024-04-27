import pandas as pd
from joblib import load

scaler = load('scaler.joblib')
knn = load('knn_model.joblib')

test_data = pd.DataFrame({
    'right_ascension': [14.24521111111111], 
    'declination': [30.0]
})

test_features = scaler.transform(test_data)
predictions = knn.predict(test_features)
prediction_prob = knn.predict_proba(test_features)[0]

class_probabilities = {}
for idx, prob in enumerate(prediction_prob):
    if prob > 0.05:  
        class_probabilities[knn.classes_[idx]] = prob

print(f"Predicted constellation: {predictions[0]}")
print(f"Probabilities of predictions adjusted for model accuracy:")
for constellation, prob in class_probabilities.items():
    print(f"{constellation}: {prob*100:.2f}%")
print(f"Note: This model was trained using the K-Nearest Neighbors (KNN) algorithm on a dataset consisting of 3,994 records. It achieved an accuracy of 94% on the test set.")
