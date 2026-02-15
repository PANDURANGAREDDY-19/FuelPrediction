import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2,
        'predictions': y_pred
    }

def compare_models(models, X_test, y_test):
    """Compare multiple models"""
    results = {}
    for name, model in models.items():
        metrics = evaluate_model(model, X_test, y_test)
        results[name] = {k: v for k, v in metrics.items() if k != 'predictions'}
    
    return results

if __name__ == "__main__":
    import pandas as pd
    import os
    import sys
    
    # Add src to path and set correct working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    sys.path.insert(0, script_dir)
    os.chdir(project_root)
    
    from feature_engineering import engineer_features, prepare_data
    from model import train_models
    
    df = pd.read_csv('data/raw/fuel_data.csv')
    df = engineer_features(df)
    X, y, _ = prepare_data(df)
    
    trained_models, _, X_test, _, y_test = train_models(X, y)
    results = compare_models(trained_models, X_test, y_test)
    
    print("\n📊 MODEL COMPARISON")
    print("="*60)
    for model_name, metrics in results.items():
        print(f"\n{model_name}:")
        for metric, value in metrics.items():
            print(f"  {metric}: {value:.4f}")
