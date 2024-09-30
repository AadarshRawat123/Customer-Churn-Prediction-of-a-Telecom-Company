# -*- coding: utf-8 -*-
"""Project 1: Customer Churn Prediction of a Telecom Company

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1wPUD5eAKRmo-F8mRjmA89xTg4b7XdGay

# 1. Data Cleaning
# Start with Importing important libraries:
"""

import numpy as np    # linear algebra
import pandas as pd   # data processing
import seaborn as sns # For creating plots
import matplotlib.ticker as mtick # For specifying axes tick format
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
sns.set(style = 'white')

# Read the data from the file "churn_data.csv" and store it in the variable "df"
df = pd.read_csv("/content/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Print the shape of the DataFrame
print(df.shape)

"""# Converting columns in the required datatype format before moving forward. As “TotalCharges” column is defined as object which is originally a numerical column.




"""

# Converting TotalCharges to a numerical data type.
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')

# Passed a dictionary to astype() function
df = df.astype({
    'customerID': 'category',
    'gender': 'category',
    'SeniorCitizen': 'category',
    'Partner': 'category',
    'Dependents': 'category',
    'tenure': 'category',
    'PhoneService': 'category',
    'MultipleLines': 'category',
    'InternetService': 'category',
    'OnlineSecurity': 'category',
    'OnlineBackup': 'category',
    'DeviceProtection': 'category',
    'TechSupport': 'category',
    'StreamingTV': 'category',
    'StreamingMovies': 'category',
    'Contract': 'category',
    'PaperlessBilling': 'category',
    'PaymentMethod': 'category',
    'MonthlyCharges': 'float64'
})

"""# Now First, check for any missing values available or not, and if available then by how many percentages so decide the imputation method accordingly."""

# Percentage of null values
df.isnull().sum() * 100 / len(df)

"""# Now missing is present in the dataset it is in very small percentages so either missing value can be removed from dataset or impute using simple mean imputation. There are 11 missing values which are only 0.15% of total values for Total Charges. So we can fill it with simple mean imputation our data set."""

# fill missing values with mean column values
df.TotalCharges.fillna(df.TotalCharges.mean(), inplace=True)

"""# 2. Exploratory Data Analysis
Check for imbalance class distribution
"""

# Class Distribution
df.Churn.value_counts()

"""# Plot of Churn Class Distribution"""

def bar_plot(df, column):
    ax = sns.countplot(y=column, data=df)
    plt.title('Distribution of  Configurations')
    plt.xlabel('Number of Axles')
    total = len(df[column])
    for p in ax.patches:
        percentage = '{:.1f}%'.format(100 * p.get_width() / total)
        x = p.get_x() + p.get_width() + 0.02
        y = p.get_y() + p.get_height() / 2
        ax.annotate(percentage, (x, y))
    plt.show()

bar_plot(df, "Churn")

"""# Numerical features
There are only three numerical columns: tenure, monthly charges, and total charges.
"""

def kdeplot(feature, hist, kde):
    plt.figure(figsize=(9, 4))
    plt.title("Plot for {}".format(feature))
    ax0 = sns.distplot(df[df['Churn'] == 'No'][feature].dropna(), hist=hist, kde=kde,
             color = 'darkblue',  label= 'Churn: No',
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 4})
    ax1 = sns.distplot(df[df['Churn'] == 'Yes'][feature].dropna(), hist=hist, kde=kde,
             color = 'orange',  label= 'Churn: Yes',
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 4})
    plt.savefig('kde.png')
kdeplot('tenure', hist = False, kde = True)
kdeplot('MonthlyCharges', hist = False, kde = True)
kdeplot('TotalCharges', hist = False, kde = True)

"""### From the plots above we can conclude that:
### Recent Users are more likely to churn
### Users with higher MonthlyCharges are also more likely to churn
### TotalCharges have a similar property for both

## Feature Generation that can b done by the difference between the MonthlyCharges and the TotalCharges divided by the tenure:
"""

def kdeplot(feature, hist, kde):
    plt.figure(figsize=(9, 4))
    plt.title("Plot for {}".format(feature))
    ax0 = sns.distplot(df[df['Churn'] == 'No'][feature].dropna(), hist=hist, kde=kde,
             color = 'darkblue',  label= 'Churn: No',
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 4})
    ax1 = sns.distplot(df[df['Churn'] == 'Yes'][feature].dropna(), hist=hist, kde=kde,
             color = 'orange',  label= 'Churn: Yes',
             hist_kws={'edgecolor':'black'},
             kde_kws={'linewidth': 4})
    plt.savefig('kde.png')

# Call the kdeplot function with hist and kde arguments
kdeplot('monthly_charges_diff', hist=False, kde=True)

"""# Categorical features
## This dataset has 16 categorical features:
Six binary features (Yes/No)

Nine features with three unique values each (categories)

One feature with four unique values

## Binary Features (Yes/No)
"""

# Example data (assuming df is your dataframe)
# Mapping binary features to 'Yes' and 'No'
binary_columns = ['SeniorCitizen', 'Partner', 'Dependents', 'PhoneService', 'PaperlessBilling']

for col in binary_columns:
    df[col] = df[col].map({1: 'Yes', 0: 'No', 'Yes': 'Yes', 'No': 'No'})

# Ensure 'gender' is correctly represented
df['gender'] = df['gender'].map({'Female': 'Female', 'Male': 'Male'})

# Plotting the binary features
fig, axes = plt.subplots(2, 3, figsize=(12, 7), sharey=True)
sns.countplot(x="gender", data=df, ax=axes[0, 0])
sns.countplot(x="SeniorCitizen", data=df, ax=axes[0, 1])
sns.countplot(x="Partner", data=df, ax=axes[0, 2])
sns.countplot(x="Dependents", data=df, ax=axes[1, 0])
sns.countplot(x="PhoneService", data=df, ax=axes[1, 1])
sns.countplot(x="PaperlessBilling", data=df, ax=axes[1, 2])

# Adjusting the layout
fig.tight_layout()

# Saving the figure
fig.savefig("inp.png")

# Display the plot
plt.show()

"""Gender Distribution — About half of the customers in our data set are male while the other half are female.

% Senior Citizens — There are only 16% of the customers who are senior citizens. Thus most of our customers in the data are younger people.

Partner — About 50% of the customers have a partner.

Dependent status — Only 30% of the total customers have dependents.

Phone Service — About 90.3% of the customers have phone services.

Paperless Billing— About 59.2% of the customers make paperless billing

## Partner and Dependent:
"""

# Reshape the data into a long-form format
df_long = df.melt(id_vars=["Partner"], value_vars=["Dependents"])

# Create the countplot with hue
sns.countplot(x="Partner", hue="value", data=df_long)

#Ensure 'Partner' and 'Dependents' are correctly mapped if needed
df['Partner'] = df['Partner'].map({'Yes': 'Yes', 'No': 'No', 1: 'Yes', 0: 'No'})
df['Dependents'] = df['Dependents'].map({'Yes': 'Yes', 'No': 'No', 1: 'Yes', 0: 'No'})

# Create subplots
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# Set titles for the subplots
axes[0].set_title("Has partner")
axes[1].set_title("Has dependents")
axis_y = "percentage of customers"

# Plot Partner column
gp_partner = df.groupby(['Partner', 'Churn']).size() / len(df)
gp_partner = gp_partner.to_frame().rename({0: axis_y}, axis=1).reset_index()
sns.barplot(x='Partner', y=axis_y, hue='Churn', data=gp_partner, ax=axes[0])

# Plot Dependents column
gp_dep = df.groupby(['Dependents', 'Churn']).size() / len(df)
gp_dep = gp_dep.to_frame().rename({0: axis_y}, axis=1).reset_index()
sns.barplot(x='Dependents', y=axis_y, hue='Churn', data=gp_dep, ax=axes[1])

# Adjust layout
fig.tight_layout()

# Save the figure
fig.savefig("inp.png")

# Display the plot
plt.show()

"""Customer who has Partner is more likely to have Dependent

Customers that don’t have Partners are more likely to churn

Customers without Dependents are also more likely to churn

## Senior Citizens and Dependent:
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data (replace 'path/to/your/dataset.csv' with the actual path to your dataset)
df = pd.read_csv('/content/WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Ensure binary columns are correctly mapped
df['SeniorCitizen'] = df['SeniorCitizen'].map({1: 'Yes', 0: 'No'})
df['Dependents'] = df['Dependents'].map({'Yes': 'Yes', 'No': 'No', 1: 'Yes', 0: 'No'})

# Create the count plot
sns.countplot(x="SeniorCitizen", data=df, hue='Dependents')

# Show the plot
plt.show()

"""Senior Citizen is less likely to have Dependent

# Phone and Internet services
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the bar_plot function
def bar_plot(df, column):
    plt.figure(figsize=(8, 6))
    sns.countplot(x=column, data=df)
    plt.title(f'Count Plot for {column}')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.show()

# Load your data (replace 'path/to/your/dataset.csv' with the actual path to your dataset)
df = pd.read_csv('/content/WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Ensure binary columns are correctly mapped if needed
df['MultipleLines'] = df['MultipleLines'].map({'Yes': 'Yes', 'No': 'No', 'No phone service': 'No phone service'})

# Call the bar_plot function with the DataFrame and the column name
bar_plot(df, "MultipleLines")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data (replace 'path/to/your/dataset.csv' with the actual path to your dataset)
df = pd.read_csv('/content/WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Ensure binary columns are correctly mapped if needed
df['MultipleLines'] = df['MultipleLines'].map({'Yes': 'Yes', 'No': 'No', 'No phone service': 'No phone service'})
df['Churn'] = df['Churn'].map({'Yes': 'Yes', 'No': 'No', 1: 'Yes', 0: 'No'})

# Create the count plot
plt.figure(figsize=(8, 6))
sns.countplot(x="MultipleLines", data=df, hue="Churn")
plt.title('Count Plot for MultipleLines by Churn')
plt.xlabel('MultipleLines')
plt.ylabel('Count')
plt.show()

"""Few customers don’t have phone service

Customers with multiple lines have a slightly higher churn rate
"""

bar_plot(df, "InternetService")

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load your data (replace 'path/to/your/dataset.csv' with the actual path to your dataset)
df = pd.read_csv('/content/WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Ensure binary columns are correctly mapped if needed
# Assuming 'InternetService' and 'Churn' are correctly formatted and no need for mapping

# Create the count plot
plt.figure(figsize=(8, 6))
sns.countplot(x="InternetService", data=df, hue="Churn")
plt.title('Count Plot for InternetService by Churn')
plt.xlabel('InternetService')
plt.ylabel('Count')
plt.show()

"""Customers without internet have a very low churn rate

Customers with fiber are more probable to churn than those with a DSL connection

# Internet Services

## There are six additional services for customers with the internet:

OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies
"""

cols = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
df1 = pd.melt(df[df["InternetService"] != "No"][cols]).rename({'value': 'Has service'}, axis=1)
plt.figure(figsize=(10, 4.5))
ax = sns.countplot(data=df1, x='variable', hue='Has service')
ax.set(xlabel='Additional service', ylabel='Num of customers')
plt.show()

"""Customers with the first 4 additionals (security to tech support) are more unlikely to churn

Streaming service is not predictive for churn

# Payment Method
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Define the bar_plot function
def bar_plot(df, column):
    plt.figure(figsize=(10, 6))
    sns.countplot(x=column, data=df)
    plt.title(f'Count Plot for {column}')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.xticks(rotation=45)  # Rotate x labels if necessary
    plt.show()

# Load your data (replace 'path/to/your/dataset.csv' with the actual path to your dataset)
df = pd.read_csv('/content/WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Ensure the PaymentMethod column is correctly formatted if needed
# Example: df['PaymentMethod'] = df['PaymentMethod'].map(...)

# Call the bar_plot function with the DataFrame and the column name
bar_plot(df, "PaymentMethod")

df = pd.read_csv('/content/WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Ensure columns are correctly formatted if needed
# Example: df['PaymentMethod'] = df['PaymentMethod'].map(...)

# Create the count plot
plt.figure(figsize=(10, 6))
sns.countplot(x="PaymentMethod", data=df, hue="Churn")
plt.title('Count Plot for PaymentMethod by Churn')
plt.xlabel('PaymentMethod')
plt.ylabel('Count')
plt.xticks(rotation=45)  # Rotate x labels if necessary
plt.show()

"""Electronic Check is the Largest Payment method

Electronic Check has most churn in Payment Method

# **Correlation Between Features**
"""

df = pd.read_csv('/content/WA_Fn-UseC_-Telco-Customer-Churn.csv')

# Check if the columns exist before dropping them
columns_to_drop = ['customerID', 'total_charges_to_tenure_ratio', 'monthly_charges_diff']
existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
df.drop(existing_columns_to_drop, axis=1, inplace=True)

# Factorize the DataFrame and compute the correlation matrix
df_corr = df.apply(lambda x: pd.factorize(x)[0] if x.dtype == 'object' else x)
corr_matrix = df_corr.corr()

# Create the heatmap
plt.figure(figsize=(12, 6))
ax = sns.heatmap(corr_matrix, xticklabels=corr_matrix.columns, yticklabels=corr_matrix.columns,
                 linewidths=.2, cmap="YlGnBu")
plt.title('Correlation Heatmap')
plt.show()

plt.figure(figsize=(15, 10))
sns.heatmap(df_corr.corr(), annot=True)

"""# **Oversampling Technique**

Synthetic Minority Oversampling Technique(SMOTE) is an oversampling technique and widely used to handle the imbalanced dataset. This technique synthesizes new data points for minority class and oversample that class.
"""

from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state=0)
X_resampled, y_resampled = sm.fit_resample(x, y)
y_resampled.value_counts()

"""# **Train Test Split**

Divides data into Train and Test Subset
"""

# Import the necessary module
from sklearn.model_selection import train_test_split

# Resample the data using SMOTE
from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state=0)
X_resampled, y_resampled = sm.fit_resample(x, y)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_resampled, y_resampled, test_size = 0.2, random_state=42)

"""# **Model**

### For Starter, the GradientBoostingClassifier model is implemented to show to results of the basic model and its predictions.
"""

from sklearn.ensemble import GradientBoostingClassifier
# Check if there is a variable named 'GradientBoostingClassifier'
if 'GradientBoostingClassifier' in globals():
    del globals()['GradientBoostingClassifier']

# Import the GradientBoostingClassifier class again
from sklearn.ensemble import GradientBoostingClassifier

"""# **Train Predict**

### Model prediction on the training dataset
"""

pred = clf_forest.predict(X_train)
accuracy_score(y_train, pred)

"""# **Test Predict**

### Model prediction in testing dataset
"""

pred_test = clf_forest.predict(X_test)
accuracy_score(y_test, pred_test)