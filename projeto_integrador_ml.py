# -*- coding: utf-8 -*-
"""Projeto_Integrador_ML.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gWmYcIzvbqhTDYVcryMjzRimd1BZDeVi

# IMPORTAÇÃO DE BIBLIOTECAS
"""
import streamlit as st
# !pip install catboost
import numpy as np 
import pandas as pd 
# import seaborn as sns
# import matplotlib as mpl
# import matplotlib.pyplot as plt
# import matplotlib.pylab as pylab
# from catboost import CatBoostRegressor
# from sklearn.preprocessing import OneHotEncoder, LabelEncoder
# from sklearn.model_selection import train_test_split
# from sklearn.datasets import make_regression
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# from sklearn.pipeline import Pipeline
# from sklearn.tree import DecisionTreeRegressor
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.linear_model import LinearRegression
# from xgboost import XGBRegressor
# from sklearn.neighbors import KNeighborsRegressor
# from sklearn.model_selection import cross_val_score
# from sklearn.metrics import mean_squared_error
# from sklearn import metrics

"""# IMPORTAÇÃO DO DATASET"""

df = pd.read_csv('/content/diamonds.csv', delimiter=',')
df

df.head()

df.shape

"""# PRÉ PROCESSAMENTO DE DADOS"""

#informações da tabela
df.info()

#retirada das informações desnecessárias da primeira coluna
df = df.drop(["Unnamed: 0"], axis=1)
df.describe()

#retirada dos diamantes sem dimensão 
df = df.drop(df[df["x"]==0].index)
df = df.drop(df[df["y"]==0].index)
df = df.drop(df[df["z"]==0].index)
df.shape

#teste de regressão simples
x,y = make_regression(n_samples=200, n_features=1, noise=30)
plt.scatter(x,y)

#preços
ns.boxplot(df.price,)

sns.pairplot(df)

#retirada de dados de ruído
df = df[(df["depth"]<75)&(df["depth"]>45)]
df = df[(df["table"]<80)&(df["table"]>40)]
df = df[(df["x"]<30)]
df = df[(df["y"]<30)]
df = df[(df["z"]<30)&(df["z"]>2)]
df.shape

#limpando
sns.pairplot(df, hue= "cut")

s = (df.dtypes =="object")
object_cols = list(s[s].index)
print("Categorical variables:")
print(object_cols)

# Make copy to avoid changing original data 
label_df = df.copy()

# Apply label encoder to each column with categorical data
label_encoder = LabelEncoder()
for col in object_cols:
    label_df[col] = label_encoder.fit_transform(label_df[col])
label_df.head()

#matriz de correlação
cmap = sns.diverging_palette(70,20,s=50, l=40, n=6,as_cmap=True)
corrmat= label_df.corr()
f, ax = plt.subplots(figsize=(12,12))
sns.heatmap(corrmat,cmap=cmap,annot=True, )

"""# CRIAÇÃO DO MODELO DE PREDIÇÃO"""

X= df.drop(["price"],axis =1)
y= df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.25, random_state=7)
categorical_features_indices = np.where(X.dtypes !=float)[0]

X= label_df.drop(["price"],axis =1)
y= label_df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.25, random_state=7)

pipeline_lr=Pipeline([("scalar1",StandardScaler()),
                     ("lr_classifier",LinearRegression())])

pipeline_dt=Pipeline([("scalar2",StandardScaler()),
                     ("dt_classifier",DecisionTreeRegressor())])

pipeline_rf=Pipeline([("scalar3",StandardScaler()),
                     ("rf_classifier",RandomForestRegressor())])

pipeline_kn=Pipeline([("scalar4",StandardScaler()),
                     ("rf_classifier",KNeighborsRegressor())])

pipeline_xgb=Pipeline([("scalar5",StandardScaler()),
                     ("rf_classifier",XGBRegressor())])

pipelines = [pipeline_lr, pipeline_dt, pipeline_rf, pipeline_kn, pipeline_xgb]

pipe_dict = {0: "LinearRegression", 1: "DecisionTree", 2: "RandomForest",3: "KNeighbors", 4: "XGBRegressor"}

for pipe in pipelines:
    pipe.fit(X_train, y_train)

model = CatBoostRegressor(iterations=50, depth=3, learning_rate=0.1, loss_function='RMSE')

model.fit(X_train, y_train,
          
          cat_features=categorical_features_indices,

          eval_set=(X_test, y_test),plot=True
    
)

"""# AVALIAÇÃO DA MAQUINA PREDITIVA"""

print(model.get_best_iteration())

pred = pipeline_xgb.predict(X_test)

print("R^2:",metrics.r2_score(y_test, pred))
print("Adjusted R^2:",1 - (1-metrics.r2_score(y_test, pred))*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1))
print("MAE:",metrics.mean_absolute_error(y_test, pred))
print("MSE:",metrics.mean_squared_error(y_test, pred))
print("RMSE:",np.sqrt(metrics.mean_squared_error(y_test, pred)))
