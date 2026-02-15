import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
import joblib

def train_models(X, y):
    """Train multiple regression models"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': XGBRegressor(n_estimators=100, random_state=42)
    }
    
    trained_models = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        trained_models[name] = model
        print(f"✓ {name} trained")
    
    return trained_models, X_train, X_test, y_train, y_test

def save_model(model, filename):
    """Save trained model"""
    joblib.dump(model, filename)
    print(f"✓ Model saved: {filename}")

if __name__ == "__main__":
    import os
    import sys
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    sys.path.insert(0, script_dir)
    os.chdir(project_root)
    
    from feature_engineering import engineer_features, prepare_data
    
    df = pd.read_csv('data/raw/fuel_data.csv')
    df = engineer_features(df)
    X, y, scaler = prepare_data(df)
    
    trained_models, X_train, X_test, y_train, y_test = train_models(X, y)
    
    save_model(trained_models['XGBoost'], 'models/xgboost_model.pkl')
    save_model(scaler, 'models/scaler.pkl')
