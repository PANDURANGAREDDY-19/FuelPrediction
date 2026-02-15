import sqlite3
import pandas as pd
from datetime import datetime
import os

class PredictionDatabase:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        db_path = os.path.join(project_root, 'data', 'predictions.db')
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_table()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                vehicle_type TEXT,
                engine_capacity REAL,
                fuel_type TEXT,
                distance REAL,
                load_weight REAL,
                road_type TEXT,
                avg_speed REAL,
                traffic_level TEXT,
                mileage_category TEXT,
                predicted_fuel REAL,
                fuel_price REAL,
                total_cost REAL,
                mileage_kmpl REAL,
                co2_emissions REAL
            )
        ''')
        self.conn.commit()
    
    def save_prediction(self, data):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO predictions (
                timestamp, vehicle_type, engine_capacity, fuel_type, distance,
                load_weight, road_type, avg_speed, traffic_level, mileage_category,
                predicted_fuel, fuel_price, total_cost, mileage_kmpl, co2_emissions
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data['vehicle_type'], data['engine_capacity'], data['fuel_type'],
            data['distance'], data['load_weight'], data['road_type'],
            data['avg_speed'], data['traffic_level'], data['mileage_category'],
            data['predicted_fuel'], data['fuel_price'], data['total_cost'],
            data['mileage_kmpl'], data['co2_emissions']
        ))
        self.conn.commit()
    
    def get_all_predictions(self):
        df = pd.read_sql_query("SELECT * FROM predictions ORDER BY timestamp DESC", self.conn)
        # Convert numeric columns to proper types
        numeric_cols = ['engine_capacity', 'distance', 'load_weight', 'avg_speed', 
                       'predicted_fuel', 'fuel_price', 'total_cost', 'mileage_kmpl', 'co2_emissions']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    
    def get_recent_predictions(self, limit=10):
        df = pd.read_sql_query(f"SELECT * FROM predictions ORDER BY timestamp DESC LIMIT {limit}", self.conn)
        # Convert numeric columns to proper types
        numeric_cols = ['engine_capacity', 'distance', 'load_weight', 'avg_speed', 
                       'predicted_fuel', 'fuel_price', 'total_cost', 'mileage_kmpl', 'co2_emissions']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        return df
    
    def get_statistics(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*), AVG(predicted_fuel), AVG(total_cost), SUM(co2_emissions) FROM predictions")
        result = cursor.fetchone()
        return {
            'total_predictions': result[0] or 0,
            'avg_fuel': result[1] or 0,
            'avg_cost': result[2] or 0,
            'total_co2': result[3] or 0
        }
    
    def clear_history(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM predictions")
        self.conn.commit()
    
    def close(self):
        self.conn.close()
