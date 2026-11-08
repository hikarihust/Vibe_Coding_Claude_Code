# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Diabetes risk prediction app using the Pima Indians Diabetes dataset. A Logistic Regression model is trained on health metrics and served via a Gradio web interface. The UI is in Vietnamese.

## Commands

Run all commands from the project root: modules import each other as `src.*`, so `python src/train.py` fails — use `python -m src.train`. A local virtualenv (Python 3.13) lives in `.venv/` (Windows: `.venv\Scripts\activate`).

```bash
# Install dependencies
pip install -r requirements.txt

# Train/retrain the model (saves model.joblib and scaler.joblib to models/)
python -m src.train

# Run the Gradio web app
python app.py
```

## Architecture

The pipeline flows: **raw CSV → data prep → train → serialized model → predict → Gradio UI**.

- `src/data_preparation.py` — Loads `data/raw/diabetes.csv`, replaces biologically implausible zeros with median values (for Glucose, BloodPressure, SkinThickness, Insulin, BMI), splits train/val with stratification, and fits a `StandardScaler`. The 8 feature columns and target column are defined here as constants (`FEATURE_COLUMNS`, `TARGET_COLUMN`).
- `src/train.py` — Calls `prepare_data()`, trains `LogisticRegression`, prints validation metrics, and serializes both model and scaler to `models/`.
- `src/predict.py` — Loads the serialized model+scaler and exposes `predict(input_dict)` which accepts a dict keyed by feature column names and returns prediction, label, and probabilities.
- `app.py` — Gradio interface that maps `gr.Number` inputs to `predict()`. Feature metadata is defined in `FEATURE_INFO` as tuples `(column, vietnamese_label, min, max, step, default)`; `step` is currently unused.

The model and scaler are always loaded fresh from disk on each prediction call (no caching), so retraining takes effect without restarting the app.

## Gotchas

- **Train/serve skew:** `predict()` does not call `clean_data()`. A 0 entered for Glucose/BloodPressure/SkinThickness/Insulin/BMI goes straight to the scaler instead of being median-imputed as in training, and the UI allows 0 for those fields.
- **Feature order:** `predict()` builds the feature vector by iterating `FEATURE_COLUMNS`, not `FEATURE_INFO`; `classify()` maps UI args to columns by `FEATURE_INFO` position. Adding/removing a feature requires updating both lists and retraining.
- There are no tests or linter configured.
