import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

# Load the data
nfl_data = pd.read_csv('downloads/pbp-2023.csv')

# Filter for 2-point conversions
two_point_data = nfl_data[nfl_data['IsTwoPointConversion'] == 1]

# Select notable columns for study
two_point_data_filtered = two_point_data[['PlayType', 'RushDirection', 'PassType', 'IsTwoPointConversionSuccessful']]
two_point_data_filtered.fillna('None', inplace=True)

# Encode
label_encoder = LabelEncoder()
two_point_data_encoded = two_point_data_filtered.apply(label_encoder.fit_transform)

# Define features and target
X = two_point_data_encoded[['PlayType', 'RushDirection', 'PassType']]
y = two_point_data_encoded['IsTwoPointConversionSuccessful']

# Split the data into test and train datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=43)

# Initialize and train the model
model = RandomForestClassifier(random_state=43)
model.fit(X_train, y_train)

# Predict and print the accuracy for evaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

