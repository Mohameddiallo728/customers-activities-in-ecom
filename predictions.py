import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor

df = pd.read_csv("data/bamako_hourly-2000_2023.csv")


def linearRegression(df):
    features = df.drop(['temperature_2m', 'date'], axis=1)
    target = df['temperature_2m']  # Assurez-vous que la casse est correcte ici

    # Division des données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

    # Normalisation des données (facultatif, mais souvent recommandé)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Création et entraînement du modèle
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)

    # Prédictions sur l'ensemble de test
    predictions = model.predict(X_test_scaled)

    # Évaluation du modèle
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    return [y_test, predictions, mse, r2]


def xgBoost(df):
    features = df.drop(['temperature_2m', 'date'], axis=1)
    target = df['temperature_2m']  # Assurez-vous que la casse est correcte ici

    # Division des données en ensembles d'entraînement et de test
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.3, random_state=42)

    # Normalisation des données (facultatif, mais souvent recommandé)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    xgb_model = XGBRegressor()
    xgb_model.fit(X_train_scaled, y_train)

    # Prédictions sur l'ensemble de test
    xgb_predictions = xgb_model.predict(X_test_scaled)
    residuals = y_test - xgb_predictions

    # Évaluation du modèle XGBoost
    xgb_mse = mean_squared_error(y_test, xgb_predictions)
    xgb_rmse = np.sqrt(xgb_mse)
    xgb_r2 = r2_score(y_test, xgb_predictions)
    return [y_test, xgb_predictions, xgb_mse, xgb_r2]
