# 🚀 Quick Start Guide - Fuel Consumption Prediction System

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- 2GB free disk space

---

## Installation & Setup (5 minutes)

### Step 1: Navigate to Project Directory
```bash
cd d:\PythonProject\Fuel_Consumption_Prediction
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected Output**: All packages installed successfully

---

## Running the Project

### Option A: Complete Pipeline (Recommended for First Time)

#### 1. Generate Data
```bash
cd src
python data_generation.py
```
**Output**: Creates `data/raw/fuel_data.csv` (1000 records)

#### 2. Engineer Features
```bash
python feature_engineering.py
```
**Output**: Creates `data/processed/fuel_data_processed.csv`

#### 3. Train Models
```bash
python model.py
```
**Output**: 
```
✓ Linear Regression trained
✓ Random Forest trained
✓ XGBoost trained
✓ Model saved: ../models/xgboost_model.pkl
✓ Model saved: ../models/scaler.pkl
```

#### 4. Evaluate Models
```bash
python evaluation.py
```
**Output**: Performance comparison table with MAE, MSE, RMSE, R²

#### 5. Launch Web App
```bash
cd ../app
streamlit run app.py
```
**Output**: Opens browser at `http://localhost:8501`

---

### Option B: Jupyter Notebooks (For Exploration)

#### 1. Start Jupyter
```bash
cd notebooks
jupyter notebook
```

#### 2. Open Notebooks
- `EDA.ipynb` - Exploratory Data Analysis with visualizations
- `Model_Training.ipynb` - Model training and comparison

---

## Using the Web App

### Input Parameters
1. **Vehicle Type**: Car, Van, Bus, or Truck
2. **Engine Capacity**: 1.5 - 5.0 liters
3. **Fuel Type**: Diesel, Petrol, or CNG
4. **Distance**: 10 - 500 km
5. **Load Weight**: 0 - 5000 kg
6. **Road Type**: Highway, City, or Mixed
7. **Average Speed**: 20 - 120 km/h
8. **Traffic Level**: Low, Medium, or High

### Example Prediction
**Input**:
- Vehicle: Truck
- Engine: 4.5L
- Fuel: Diesel
- Distance: 250 km
- Load: 3000 kg
- Road: Highway
- Speed: 70 km/h
- Traffic: Low

**Output**: Predicted Fuel: ~45.2 Liters

---

## Troubleshooting

### Issue: Module not found
**Solution**: 
```bash
pip install -r requirements.txt
```

### Issue: Model not found in web app
**Solution**: Run `python src/model.py` first to train and save the model

### Issue: Jupyter kernel not found
**Solution**: 
```bash
python -m ipykernel install --user
```

---

## Project Structure Verification

Run this to verify all files are created:
```bash
dir /s /b
```

**Expected Files**:
- ✅ requirements.txt
- ✅ README.md
- ✅ src/data_generation.py
- ✅ src/feature_engineering.py
- ✅ src/model.py
- ✅ src/evaluation.py
- ✅ app/app.py
- ✅ notebooks/EDA.ipynb
- ✅ notebooks/Model_Training.ipynb
- ✅ reports/insights_report.md

---

## Expected Results

### Model Performance
| Model | R² Score | RMSE |
|-------|----------|------|
| Linear Regression | ~0.85 | ~4.2 |
| Random Forest | ~0.94 | ~2.8 |
| XGBoost | ~0.96 | ~2.4 |

### Key Insights
- Distance is the strongest predictor (40% importance)
- Heavy loads increase fuel by 10-15%
- High traffic increases consumption by 30%
- Highway roads are 10% more efficient

---

## Next Steps

1. ✅ Run the complete pipeline
2. ✅ Explore notebooks for visualizations
3. ✅ Test the web app with different inputs
4. ✅ Read `reports/insights_report.md` for business insights
5. ✅ Prepare for viva using README.md Q&A section

---

## Support

For issues or questions:
1. Check README.md for detailed documentation
2. Review insights_report.md for business context
3. Examine code comments in src/ files

---

**Estimated Time**: 
- Setup: 5 minutes
- Data generation & training: 2 minutes
- Exploration: 15-30 minutes
- **Total**: ~20-40 minutes

**Good luck with your project! 🚀**
