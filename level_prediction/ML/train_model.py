import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from level_prediction.models import Features  # Assuming your model is named 'Features'

# Fetch data from the database using Django ORM
data = Features.objects.all().values()
df = pd.DataFrame(list(data))

# Verify the first few rows of the data to ensure it's correct
print(df.head())

# Prepare features (X) and target (y)
X = df.drop(columns=['Experience_Level'])
y = df['Experience_Level']  # No encoding needed for target variable since it contains 1, 2, or 3

# Encode the categorical features in X (if any)
label_encoders = {}
for col in X.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col])
    label_encoders[col] = le

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print('Training X: ', X_train.shape)
print('Training y: ', y_train.shape)
print('Test X: ', X_test.shape)
print('Test y: ', y_test.shape)

# Normalize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Create and train the SVM model
svm_model = SVC(kernel='sigmoid', random_state=42)
svm_model.fit(X_train, y_train)

# Predict on the test set
y_pred = svm_model.predict(X_test)

# Evaluate the model
print("Classification Report:")
print(classification_report(y_test, y_pred))

print("\nAccuracy Score:")
print(accuracy_score(y_test, y_pred))

accuracy_percentage = accuracy_score(y_test, y_pred) * 100

# Display the accuracy with a percentage symbol
print("\nAccuracy Score:")
print(f"{accuracy_percentage:.2f}%")

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['1', '2', '3'], yticklabels=['1', '2', '3'])
plt.title('Confusion Matrix', fontsize=16)
plt.xlabel('Predicted', fontsize=12)
plt.ylabel('Actual', fontsize=12)
plt.show()

# Map encoded values to experience levels
experience_level_map = {1: 'Beginner', 2: 'Intermediate', 3: 'Advanced'}

# Display the experience level for each encoded value
for encoded_value in set(y):  # set(y) gives unique values in y
    experience_level = experience_level_map.get(encoded_value, "Unknown")
    print(f"Encoded value {encoded_value} corresponds to {experience_level}")
