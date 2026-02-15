import pandas as pd
import numpy as np

def generate_fuel_data(n_samples=1000):
    """Generate synthetic fuel consumption dataset"""
    np.random.seed(42)
    
    data = {
        'vehicle_type': np.random.choice(['Truck', 'Van', 'Bus', 'Car'], n_samples),
        'engine_capacity': np.random.uniform(1.5, 5.0, n_samples),
        'fuel_type': np.random.choice(['Diesel', 'Petrol', 'CNG'], n_samples),
        'distance_km': np.random.uniform(10, 500, n_samples),
        'load_weight_kg': np.random.uniform(0, 5000, n_samples),
        'road_type': np.random.choice(['Highway', 'City', 'Mixed'], n_samples),
        'avg_speed_kmh': np.random.uniform(20, 120, n_samples),
        'traffic_level': np.random.choice(['Low', 'Medium', 'High'], n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Calculate fuel consumption based on realistic factors
    base_consumption = df['distance_km'] / 15
    
    vehicle_factor = df['vehicle_type'].map({'Car': 1.0, 'Van': 1.3, 'Bus': 1.8, 'Truck': 2.0})
    engine_factor = df['engine_capacity'] / 2.5
    load_factor = 1 + (df['load_weight_kg'] / 10000)
    road_factor = df['road_type'].map({'Highway': 0.9, 'Mixed': 1.0, 'City': 1.2})
    speed_factor = 1 + np.abs(df['avg_speed_kmh'] - 70) / 100
    traffic_factor = df['traffic_level'].map({'Low': 1.0, 'Medium': 1.15, 'High': 1.3})
    
    df['fuel_consumed_liters'] = (base_consumption * vehicle_factor * engine_factor * 
                                   load_factor * road_factor * speed_factor * traffic_factor)
    
    df['fuel_consumed_liters'] += np.random.normal(0, 2, n_samples)
    df['fuel_consumed_liters'] = df['fuel_consumed_liters'].clip(lower=1)
    
    # Calculate mileage (km per liter)
    df['mileage_kmpl'] = df['distance_km'] / df['fuel_consumed_liters']
    
    # Categorize mileage: Low (<8), Medium (8-12), High (>12)
    df['mileage_category'] = pd.cut(df['mileage_kmpl'], 
                                     bins=[0, 8, 12, float('inf')],
                                     labels=['Low', 'Medium', 'High'])
    
    return df

if __name__ == "__main__":
    import os
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    df = generate_fuel_data(1000)
    df.to_csv('data/raw/fuel_data.csv', index=False)
    print("✓ Synthetic data generated successfully!")
    print(f"Shape: {df.shape}")
    print(df.head())
