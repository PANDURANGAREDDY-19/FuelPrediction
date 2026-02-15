import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def engineer_features(df):
    """Encode categorical variables and scale features"""
    df = df.copy()
    
    le_vehicle = LabelEncoder()
    le_fuel = LabelEncoder()
    le_road = LabelEncoder()
    le_traffic = LabelEncoder()
    le_mileage = LabelEncoder()
    
    df['vehicle_type_encoded'] = le_vehicle.fit_transform(df['vehicle_type'])
    df['fuel_type_encoded'] = le_fuel.fit_transform(df['fuel_type'])
    df['road_type_encoded'] = le_road.fit_transform(df['road_type'])
    df['traffic_level_encoded'] = le_traffic.fit_transform(df['traffic_level'])
    df['mileage_category_encoded'] = le_mileage.fit_transform(df['mileage_category'])
    
    df['load_per_km'] = df['load_weight_kg'] / df['distance_km']
    df['engine_load_ratio'] = df['engine_capacity'] * df['load_weight_kg'] / 1000
    
    return df

def prepare_data(df):
    """Prepare features and target for modeling"""
    feature_cols = ['engine_capacity', 'distance_km', 'load_weight_kg', 'avg_speed_kmh',
                    'vehicle_type_encoded', 'fuel_type_encoded', 'road_type_encoded', 
                    'traffic_level_encoded', 'mileage_category_encoded', 'load_per_km', 
                    'engine_load_ratio']
    
    X = df[feature_cols]
    y = df['fuel_consumed_liters']
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=feature_cols)
    
    return X_scaled, y, scaler

if __name__ == "__main__":
    import os
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    df = pd.read_csv('data/raw/fuel_data.csv')
    df_processed = engineer_features(df)
    df_processed.to_csv('data/processed/fuel_data_processed.csv', index=False)
    print("✓ Feature engineering completed!")
