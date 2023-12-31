# -*- coding: utf-8 -*-
"""House Price Prediction .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MY_x4fNc3cZNS77RVKYsceqgaIT3t8jy
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

dataset = pd.read_excel("/content/HousePricePrediction.xlsx")

# Printing first 5 records of the dataset
print(dataset.head(5))

dataset.shape

"""
Data Preprocessing

"""

obj = (dataset.dtypes == 'object')
object_cols = list(obj[obj].index)
print("Categorical variables:",len(object_cols))

int_ = (dataset.dtypes == 'int')
num_cols = list(int_[int_].index)
print("Integer variables:",len(num_cols))

fl = (dataset.dtypes == 'float')
fl_cols = list(fl[fl].index)
print("Float variables:",len(fl_cols))

"""Exploratory Data Analysis"""

plt.figure(figsize=(12, 6))
sns.heatmap(dataset.corr(),
			cmap = 'BrBG',
			fmt = '.2f',
			linewidths = 2,
			annot = True)

"""Barplot"""

unique_values = []
for col in object_cols:
  unique_values.append(dataset[col].unique().size)
plt.figure(figsize=(10,6))
plt.title('No. Unique values of Categorical Features')
plt.xticks(rotation=90)
sns.barplot(x=object_cols,y=unique_values)

"""The plot shows that Exterior1st has around 16 unique categories and other features have around  6 unique categories. To findout the actual count of each category we can plot the bargraph of each four features separately."""

plt.figure(figsize=(18, 36))
plt.title('Categorical Features: Distribution')
plt.xticks(rotation=90)
index = 1

for col in object_cols:
	y = dataset[col].value_counts()
	plt.subplot(11, 4, index)
	plt.xticks(rotation=90)
	sns.barplot(x=list(y.index), y=y)
	index += 1

"""Data Cleansing

dropping id coloumn
"""

dataset.drop(['Id'],axis=1,inplace=True)

"""Replacing SalePrice empty values with their mean values to make the data distribution symmetric."""

dataset['SalePrice'] = dataset['SalePrice'].fillna(dataset['SalePrice'].mean())

"""Drop records with null values"""

new_dataset = dataset.dropna()

new_dataset.isnull().sum()

from sklearn.preprocessing import OneHotEncoder

s = (new_dataset.dtypes == 'object')
object_cols = list(s[s].index)
print("Categorical variables:")
print(object_cols)
print('No. of. categorical features: ',
	len(object_cols))

OH_encoder = OneHotEncoder(sparse=False)
OH_cols = pd.DataFrame(OH_encoder.fit_transform(new_dataset[object_cols]))
OH_cols.index = new_dataset.index

df_final = new_dataset.drop(object_cols, axis=1)
df_final = pd.concat([df_final, OH_cols], axis=1)

"""Splitting Dataset into Training and Testing"""

from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

X = df_final.drop(['SalePrice'], axis=1)
Y = df_final['SalePrice']

# Split the training set into training and validation set
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

"""**Model and Accuracy**

As we have to train the model to determine the continuous values, so we will be using Linear regression model.
To calculate loss we will be using the mean_absolute_percentage_error module. It can easily be imported by using sklearn library.
"""

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error

# Convert feature column names to strings
X_train.columns = X_train.columns.astype(str)
X_test.columns = X_test.columns.astype(str)

# Create a linear regression model
model = LinearRegression()

# Train the model on the training set
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model


mae= mean_absolute_percentage_error(y_test, y_pred)
print(f'Mean Absolute Percentage  Error: {mae}')

mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')


r_squared = model.score(X_test, y_test)
print(f'R-squared: {r_squared * 100:.2f}%')

# Plotting predictions vs actual values (optional)
plt.scatter(y_test, y_pred)
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.title('Actual Prices vs Predicted Prices')
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns


y_pred = model.predict(X_test)

# Visualize actual vs predicted prices
plt.figure(figsize=(10, 6))

plt.scatter(y_test, y_pred, alpha=0.5)
plt.title('Actual Prices vs Predicted Prices')
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.show()

residuals = y_test - y_pred

# Visualize the distribution of residuals
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True)
plt.title('Distribution of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()

"""Residuals are ideally distributed around zero"""



"""Regression Plot"""

# Regression plot with a line of best fit
sns.regplot(x=y_test, y=y_pred, scatter_kws={'alpha':0.5})
plt.title('Regression Plot: Actual vs Predicted Prices')
plt.xlabel('Actual Prices')
plt.ylabel('Predicted Prices')
plt.show()

import plotly.express as px


y_pred = model.predict(X_test)

# Create a DataFrame for visualization
viz_data = pd.DataFrame({'Actual Prices': y_test, 'Predicted Prices': y_pred})

# Scatter plot with a trendline
fig = px.scatter(viz_data, x='Actual Prices', y='Predicted Prices', trendline='ols',
                 title='Actual vs Predicted House Prices')

# Distribution of residuals
residuals = y_test - y_pred
fig.add_trace(px.histogram(x=residuals, nbins=30, histnorm='probability density').data[0])

# Show the figure
fig.show()