# Accuracy : 0.8373699  (83.7%)
# Model starts from line 39

import pandas as pd 

df = pd.read_csv('dataset/cities csv/ALL.csv')

df.count().sort_values()
df = df.drop(columns=['Date','Location','Sunshine','Evaporation','Cloud3pm','Cloud9am','RISK_MM'],axis=1)  
# These columns have very less data and can be ignored

# Drop all the blank data entries
df = df.dropna()

# Replace rainfall by integral values
df['RainToday'].replace({'No': 0, 'Yes': 1},inplace = True)
df['RainTomorrow'].replace({'No': 0, 'Yes': 1},inplace = True)

df = df.drop(columns=['WindGustDir', 'WindDir3pm', 'WindDir9am'])

# Standardize ( all values range from 0 to 1)
from sklearn import preprocessing
scaler = preprocessing.MinMaxScaler()
scaler.fit(df)
df = pd.DataFrame(scaler.transform(df), index=df.index, columns=df.columns)

# Best Feature Selection
from sklearn.feature_selection import SelectKBest, chi2
X = df.loc[:,df.columns!='RainTomorrow']
y = df[['RainTomorrow']]
selector = SelectKBest(chi2, k=3)
selector.fit(X, y)
X_new = selector.transform(X)
top3 = X.columns[selector.get_support(indices=True)]

# Shuffle the dataframe in random order
df = df.sample(frac=1)

# model
X = df[['Humidity3pm','Rainfall','RainToday']]
y = df[['RainTomorrow']]

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.20)
logreg = LogisticRegression(random_state=0)
logreg.fit(X_train,y_train)
y_pred = logreg.predict(X_test)
score = accuracy_score(y_test,y_pred)
print('Accuracy :',score)
