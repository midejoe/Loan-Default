# -*- coding: utf-8 -*-
"""catboost-checkpoint.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Xyx_u-dFRxsBiaEWqhINOGXg_4Bac_q-
"""

!pip install catboost

# libraries to help with reading and manipulating data
import pandas as pd
import numpy as np

# libraries to help with data visualization
import matplotlib.pyplot as plt
import seaborn as sns

# libraries to get metrics
from sklearn import metrics

# to get different metric scores
from sklearn.metrics import (
    f1_score,
    accuracy_score,
    recall_score,
    precision_score,
    confusion_matrix,
    roc_auc_score,
    plot_confusion_matrix,
)

# to split the data
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score

# to be used for data scaling and one hot encoding
from sklearn.preprocessing import StandardScaler, MinMaxScaler, OneHotEncoder

# to impute missing values
from sklearn.impute import SimpleImputer

# to oversample and undersample data
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler

# to do hyperparameter tuning
from sklearn.model_selection import RandomizedSearchCV

# to be used for creating pipelines and personalizing them
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# to define maximum number of columns displayed in a dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows',None)

# to suppress scientific notations for a dataframe
pd.set_option("display.float_format", lambda x: "%.3f" % x)

# to help with model building
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import(
     AdaBoostClassifier,
     GradientBoostingClassifier,
     RandomForestClassifier,
     BaggingClassifier,
)

from catboost import CatBoostClassifier

# to suppress warnings
import warnings

warnings.filterwarnings("ignore")

from sklearn.tree import DecisionTreeClassifier
from sklearn import tree

from xgboost import XGBClassifier

import lightgbm as lgb

# to read the training data
df = pd.read_csv("Train_set.csv")

# to read the test data
df1 = pd.read_csv("Test_set.csv")

df.shape

df1.shape

data = df.copy()

data_test = df1.copy()

data.head()

data.tail()

data_test.tail()

df.info()

# to check for duplicate values in the training data
data.duplicated().sum()

# to check for missing values
data.isnull().sum()

data_test.job_experience.value_counts()

# to check the missing values in the test data
data_test.isnull().sum()

# to check the statistical summary of the training data
data.describe(include='number').T

"""## EDA"""

# function to plot a boxplot and a histogram along the same scale.


def histogram_boxplot(data, feature, figsize=(12, 7), kde=False, bins=None):
    """
    Boxplot and histogram combined

    data: dataframe
    feature: dataframe column
    figsize: size of figure (default (12,7))
    kde: whether to the show density curve (default False)
    bins: number of bins for histogram (default None)
    """
    f2, (ax_box2, ax_hist2) = plt.subplots(
        nrows=2,  # Number of rows of the subplot grid= 2
        sharex=True,  # x-axis will be shared among all subplots
        gridspec_kw={"height_ratios": (0.25, 0.75)},
        figsize=figsize,
    )  # creating the 2 subplots
    sns.boxplot(
        data=data, x=feature, ax=ax_box2, showmeans=True, color="violet"
    )  # boxplot will be created and a star will indicate the mean value of the column
    sns.histplot(
        data=data, x=feature, kde=kde, ax=ax_hist2, bins=bins, palette="winter"
    ) if bins else sns.histplot(
        data=data, x=feature, kde=kde, ax=ax_hist2
    )  # For histogram
    ax_hist2.axvline(
        data[feature].mean(), color="green", linestyle="--"
    )  # Add mean to the histogram
    ax_hist2.axvline(
        data[feature].median(), color="black", linestyle="-"
    )  # Add median to the histogram

for feature in num_col1:
    histogram_boxplot(df1, feature, figsize=(12, 7), kde=False, bins=None)

# to check the value counts of the target variable in the training set
data.default.value_counts(normalize=True)

"""## Data Pre-processing

### Missing values treatment
"""

df['job_experience'] = df['job_experience'].fillna(value= "6-10 years")

data_test['job_experience'] = data_test['job_experience'].fillna(value= "6-10 years")

df.isna().sum()

## Define function for grouping brand_names into categories
def get_job_exp(name):
    
        # check if brand_name is Others
    if name in ['<5 Years', '6-10 years','10+ years']:
        return 'experienced'
    
    # the rest of the categories are least common brand
    else:
        return 'inexperienced'

# to create variable that contains the brand_name category
df['job_experience'] = df['job_experience'].apply(get_job_exp)

# to create variable that contains the brand_name category
data_test['job_experience'] = data_test['job_experience'].apply(get_job_exp)

## Define function for grouping brand_names into categories
def get_home_name(name):
    
        # check if brand_name is Others
    if name in ['OTHER', 'NONE']:
        return 'no'
    # check if brand_name are most common brand
    if name in ['RENT','MORTGAGE','OWN']:
        return 'yes'
    
    # the rest of the categories are least common brand
    else:
        return

# to create variable that contains the brand_name category
df['home_ownership'] = df['home_ownership'].apply(get_home_name)

# to create variable that contains the brand_name category
data_test['home_ownership'] = data_test['home_ownership'].apply(get_home_name)

## Define function for grouping brand_names into categories
def get_veri_name(name):
    
        # check if brand_name is Others
    if name in ['Source Verified', 'Verified']:
        return 'yes'
    # check if brand_name are most common brand
    if name in ['Not Verified']:
        return 'no'
    
    # the rest of the categories are least common brand
    else:
        return

# to create variable that contains the brand_name category
df['income_verification_status'] = df['income_verification_status'].apply(get_veri_name)

# to create variable that contains the brand_name category
data_test['income_verification_status'] = data_test['income_verification_status'].apply(get_veri_name)

## Define function for grouping brand_names into categories
def get_loan_purp(name):
    
        # check if brand_name is Others
    if name in ['debt_consolidation', 'credit_card','home_improvement']:
        return 'personal'
    # check if brand_name are most common brand
    if name in ['other']:
        return 'other'
    
    # the rest of the categories are least common brand
    else:
        return

# to create variable that contains the brand_name category
df['loan_purpose'] = df['loan_purpose'].apply(get_loan_purp)

# to create variable that contains the brand_name category
data_test['loan_purpose'] = data_test['loan_purpose'].apply(get_loan_purp)

## Define function for grouping brand_names into categories
def get_state_name(name):
    
        # check if brand_name is Others
    if name in ["CA" ,"NY","TX","FL","IL","NJ","PA","OH","GA","VA","NC","MI","MD","MA","AZ","WA","CO","MN","MO","IN","CT","TN","NV","WI","AL","LA","SC","OR" ]:        
        return 'popular states'
    # check if brand_name are most common brand
    if name in ["KY","OK","KS","AR","UT","NM","WV","HI","NH" ,"RI" ,"MS" ,"DC" ,"MT" ,"DE" ,"AK" ,"WY","SD","VT","NE","ME","ND","ID" ]:
        return 'least popular states'
    
    # the rest of the categories are least common brand
    else:
        return

# to create variable that contains the brand_name category
df['state_code'] = df['state_code'].apply(get_state_name)

# to create variable that contains the brand_name category
data_test['state_code'] = data_test['state_code'].apply(get_state_name)

## Define function for grouping brand_names into categories
def get_loan_sub(name):
    
        # check if brand_name is Others
    if name in ['A1', 'A2','A3','A4','A5']:
        return 'A group'
    # check if brand_name are most common brand
    if name in ['B1', 'B2','B3','B4','B5']:
        return 'B group'
    
    if name in ['C1', 'C2','C3','C4','C5']:
        return 'C group'
    
    if name in ['D1', 'D2','D3','D4','D5']:
        return 'D group'
    
    if name in ['E1', 'E2','E3','E4','E5']:
        return 'E group'
    
    if name in ['F1', 'F2','F3','F4','F5']:
        return 'F group'
    
    if name in ['G1', 'G2','G3','G4','G5']:
        return 'G group'
    
    # the rest of the categories are least common brand
    else:
        return

# to create variable that contains the brand_name category
df['loan_subgrade'] = df['loan_subgrade'].apply(get_loan_sub)

# to create variable that contains the brand_name category
data_test['loan_subgrade'] = data_test['loan_subgrade'].apply(get_loan_sub)

for feature in df.columns: # Loop through all columns in the dataframe
    if df[feature].dtype == 'object': # Only apply for columns with categorical strings
        df[feature] = pd.Categorical(df[feature])# Replace strings with an integer
df.head()

for feature in data_test.columns: # Loop through all columns in the dataframe
    if data_test[feature].dtype == 'object': # Only apply for columns with categorical strings
        data_test[feature] = pd.Categorical(data_test[feature])# Replace strings with an integer
data_test.info()

data_test.isna().sum()

df["total_current_balance"] = df.groupby(["income_verification_status"])["total_current_balance"].transform(
        lambda x: x.fillna(x.mean())
)

data_test["total_current_balance"] = data_test.groupby(["income_verification_status"])["total_current_balance"].transform(
        lambda x: x.fillna(x.mean())
)

df["total_revolving_limit"] = df.groupby(["loan_purpose"])["total_revolving_limit"].transform(
        lambda x: x.fillna(x.mean())
)

data_test["total_revolving_limit"] = data_test.groupby(["loan_purpose"])["total_revolving_limit"].transform(
        lambda x: x.fillna(x.mean())
)

df["last_week_pay"] = df.groupby(["income_verification_status"])["last_week_pay"].transform(
        lambda x: x.fillna(x.mean())
)

data_test["last_week_pay"] = data_test.groupby(["income_verification_status"])["last_week_pay"].transform(
        lambda x: x.fillna(x.mean())
)

df['annual_income'] = df["annual_income"].transform(lambda x: x.fillna(x.mean()))
df["delinq_2yrs"]= df["delinq_2yrs"].transform(lambda x: x.fillna(x.mean()))
df["total_acc"]= df["total_acc"].transform(lambda x: x.fillna(x.mean()))

data_test['annual_income'] = data_test["annual_income"].transform(lambda x: x.fillna(x.mean()))
data_test["delinq_2yrs"]= data_test["delinq_2yrs"].transform(lambda x: x.fillna(x.mean()))
data_test["total_acc"]= data_test["total_acc"].transform(lambda x: x.fillna(x.mean()))

df["public_records"]= df["public_records"].transform(lambda x: x.fillna(x.mean()))

data_test["public_records"]= data_test["public_records"].transform(lambda x: x.fillna(x.mean()))

df.isna().sum()

data_test.isna().sum()

"""### Data Cleaning"""

df.head()

df.describe(exclude='number').T

replaceStruct = {
                "loan_term":     {"3 years": 3, "5 years": 5},
                "home_ownership":     {"no": 1, "yes": 0  },
                  "loan_purpose":     {"personal":0, "other": 1},
                  "job_experience":     {"experienced": 1, "inexperienced": 0},
                   "income_verification_status":     {"yes": 0, "no": 1 },
                    "application_type":  {"INDIVIDUAL": 1, "JOINT":2 },
                    "loan_grade": {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7},
                    "loan_subgrade": {"A group": 1.1, "B group": 2.1, "C group": 3.1, "D group": 4.1, "E group": 5.1, "F group": 6.1, "G group": 7.1},
                    "state_code": {"popular states": 0, "least popular states": 1}
                    }

df = df.replace(replaceStruct)

data_test = data_test.replace(replaceStruct)

categorical_var = np.where(df.dtypes != np.float)[0]
categorical_var

"""### Build Model"""

X = df.drop(["default","ID"],axis=1)
y = df["default"]

X_test= data_test.drop("ID",axis=1)

X.head()

X_test = X_test.replace(replaceStruct)

X_test.head()

X.info()

for feature in X.columns: # Loop through all columns in the dataframe
    if X[feature].dtype == 'int': # Only apply for columns with categorical strings
        X[feature] = X[feature].astype("float")# Replace strings with an integer
X.info()

for feature in X_test.columns: # Loop through all columns in the dataframe
    if X_test[feature].dtype == 'int': # Only apply for columns with categorical strings
        X_test[feature] = X_test[feature].astype("float")# Replace strings with an integer
X_test.info()

X.head()

categorical_var = np.where(X.dtypes != np.float )[0]
categorical_var

categorical_var_test = np.where(X_test.dtypes != np.float)[0]
categorical_var_test

# defining a function to compute different metrics to check performance of a classification model built using sklearn
def model_performance_classification_sklearn(model, predictors, target):
    """
    Function to compute different metrics to check classification model performance

    model: classifier
    predictors: independent variables
    target: dependent variable
    """

    # predicting using the independent variables
    pred = model.predict(predictors)

    acc = accuracy_score(target, pred)  # to compute Accuracy
    recall = recall_score(target, pred)  # to compute Recall
    precision = precision_score(target, pred)  # to compute Precision
    f1 = f1_score(target, pred)  # to compute F1-score

    # creating a dataframe of metrics
    df_perf = pd.DataFrame(
        {"Accuracy": acc, "Recall": recall, "Precision": precision, "F1": f1,},
        index=[0],
    )

    return df_perf

# Type of scoring used to compare parameter combinations
scorer = metrics.make_scorer(metrics.accuracy_score)

model = CatBoostClassifier(iteratons = 50, learning = 0.1, random_state=1)

model.fit(X, y, cat_features = categorical_var)

modell = [] 

modell.append(("cat", CatBoostClassifier( cat_features = categorical_var, random_state=1)))


results2=[]  # Empty list to store all model's CV scores
namess = []

for name, model in modell:
    kfold = StratifiedKFold(
        n_splits=5, shuffle=True, random_state=1
    )  # Setting number of splits equal to 5
    cv_result = cross_val_score(
        estimator=model, X=X, y=y, scoring=scorer, cv=kfold
    )
    results2.append(cv_result)
    namess.append(name)
    print("{}: {}".format(name, cv_result.mean()))

# Synthetic Minority Over Sampling Technique
sm = SMOTE(sampling_strategy=1, k_neighbors=5, random_state=1)

X_train_over, y_train_over = sm.fit_resample(X, y)

print("Before OverSampling, counts of label '1': {}".format(sum(y == 1)))
print("Before OverSampling, counts of label '0': {} \n".format(sum(y== 0)))

print("After OverSampling, counts of label '1': {}".format(sum(y_train_over == 1)))
print("After OverSampling, counts of label '0': {} \n".format(sum(y_train_over == 0)))

print("After OverSampling, the shape of X_train: {}".format(X_train_over.shape))
print("After OverSampling, the shape of y_train: {} \n".format(y_train_over.shape))

model = CatBoostClassifier(random_state=1, class_weights = [0.3,0.7],learning_rate=0.2,iterations = 6000)

model.fit(X, y, cat_features=categorical_var )

cat_train_perf = model_performance_classification_sklearn(model, X, y)
cat_train_perf

cat_train_perf1 = model_performance_classification_sklearn(model, X, y)
cat_train_perf1

pred1 = model.predict(X_test)

id = df1["ID"]

df_pred_test = pd.DataFrame({"ID": id, "default": pred1})
df_pred_test.set_index("ID",inplace=True)

df_pred_test.head()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

df_pred_test.value_counts()

import os
os.makedirs('Ass8/File',exist_ok=True)

df_pred_test.to_csv("Ass8/File/Suu5.csv")

