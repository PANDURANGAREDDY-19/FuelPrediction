"""
Fuel Consumption Prediction System - Main Pipeline
Runs the complete ML workflow from data generation to model training
"""

import os
import sys

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def main():
    print_header("🚀 FUEL CONSUMPTION PREDICTION SYSTEM")
    print("Starting complete ML pipeline...\n")
    
    # Add src to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    # Step 1: Generate Data
    print_header("Step 1: Generating Synthetic Data")
    from data_generation import generate_fuel_data
    df = generate_fuel_data(1000)
    df.to_csv('data/raw/fuel_data.csv', index=False)
    print(f"✓ Generated {len(df)} trip records")
    print(f"✓ Saved to: data/raw/fuel_data.csv")
    
    # Step 2: Feature Engineering
    print_header("Step 2: Feature Engineering")
    from feature_engineering import engineer_features
    df_processed = engineer_features(df)
    df_processed.to_csv('data/processed/fuel_data_processed.csv', index=False)
    print(f"✓ Encoded categorical variables")
    print(f"✓ Created engineered features")
    print(f"✓ Saved to: data/processed/fuel_data_processed.csv")
    
    # Step 3: Train Models
    print_header("Step 3: Training ML Models")
    from feature_engineering import prepare_data
    from model import train_models, save_model
    
    X, y, scaler = prepare_data(df_processed)
    print(f"✓ Prepared {X.shape[0]} samples with {X.shape[1]} features")
    
    trained_models, X_train, X_test, y_train, y_test = train_models(X, y)
    
    save_model(trained_models['XGBoost'], 'models/xgboost_model.pkl')
    save_model(scaler, 'models/scaler.pkl')
    
    # Step 4: Evaluate Models
    print_header("Step 4: Model Evaluation")
    from evaluation import compare_models
    
    results = compare_models(trained_models, X_test, y_test)
    
    print("\n📊 MODEL PERFORMANCE COMPARISON")
    print("-" * 60)
    print(f"{'Model':<20} {'MAE':<10} {'RMSE':<10} {'R² Score':<10}")
    print("-" * 60)
    
    for model_name, metrics in results.items():
        print(f"{model_name:<20} {metrics['MAE']:<10.4f} {metrics['RMSE']:<10.4f} {metrics['R2']:<10.4f}")
    
    print("-" * 60)
    
    # Summary
    print_header("✅ PIPELINE COMPLETED SUCCESSFULLY")
    print("📁 Generated Files:")
    print("   ✓ data/raw/fuel_data.csv")
    print("   ✓ data/processed/fuel_data_processed.csv")
    print("   ✓ models/xgboost_model.pkl")
    print("   ✓ models/scaler.pkl")
    
    print("\n🎯 Next Steps:")
    print("   1. Run 'python evaluation.py' for detailed metrics")
    print("   2. Open notebooks/EDA.ipynb for visualizations")
    print("   3. Run 'streamlit run ../app/app.py' for web interface")
    
    print("\n" + "="*60)
    print("  🎉 Ready for deployment!")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Please ensure you're running from the project root directory")
        sys.exit(1)
