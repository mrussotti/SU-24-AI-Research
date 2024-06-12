import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense

#load the dataset
file_path = r'C:\Users\matth\Downloads\Churn_Modelling.csv'
dataset = pd.read_csv(file_path)

#extracting the features and labels
X = dataset.iloc[:, 3:13].values
y = dataset.iloc[:, 13].values

#encoding categorical data
labelencoder_X_1 = LabelEncoder()
X[:, 1] = labelencoder_X_1.fit_transform(X[:, 1])
labelencoder_X_2 = LabelEncoder()
X[:, 2] = labelencoder_X_2.fit_transform(X[:, 2])

#applying one hot encoding on Geography
ct = ColumnTransformer([("Geography", OneHotEncoder(), [1])], remainder='passthrough')
X = ct.fit_transform(X)
X = X[:, 1:]  # Avoiding the dummy variable trap

#splitting the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

#feature scaling
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

def build_and_train_model(activation):
    #building the ANN
    classifier = Sequential()

    #adding the input layer and the first hidden layer
    classifier.add(Dense(units=6, activation=activation, input_dim=X_train.shape[1]))

    #adding the second hidden layer
    classifier.add(Dense(units=6, activation=activation))

    #adding the output layer
    classifier.add(Dense(units=1, activation='sigmoid'))

    #compiling the ANN
    classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    #training the ANN
    history = classifier.fit(X_train, y_train, batch_size=10, epochs=10, verbose=2, validation_data=(X_test, y_test))

    #evaluating the model on the test set
    evaluation = classifier.evaluate(X_test, y_test)
    print(f"Activation: {activation}")
    print(f"Test Loss: {evaluation[0]}")
    print(f"Test Accuracy: {evaluation[1]}")
    print("\n")
    
    return history

#test different activation functions
activations = ['relu', 'sigmoid', 'tanh']
histories = {}

for activation in activations:
    histories[activation] = build_and_train_model(activation)

#plotting the results
plt.figure(figsize=(14, 5))

#plot accuracy
plt.subplot(1, 2, 1)
for activation in activations:
    plt.plot(histories[activation].history['val_accuracy'], label=f'Val Accuracy ({activation})')
plt.title('Validation Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

# plot loss
plt.subplot(1, 2, 2)
for activation in activations:
    plt.plot(histories[activation].history['val_loss'], label=f'Val Loss ({activation})')
plt.title('Validation Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()
