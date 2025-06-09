# Machine learning model logic

"""
ml_model.py
-----------
Provides utilities to train and evaluate machine learning models for stock price movement prediction.
Includes helper functions for training an XGBoost classifier and evaluating its performance.
"""

import os
import joblib
import pandas as pd
import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix


def train_xgboost(X_train: pd.DataFrame,
                  y_train: pd.Series,
                  params: dict = None,
                  num_rounds: int = 100,
                  model_path: str = None) -> xgb.XGBClassifier:
    """
    Train an XGBoost classifier on the provided training data.

    Args:
        X_train (pd.DataFrame): Feature matrix for training.
        y_train (pd.Series): Target vector for training.
        params (dict, optional): XGBoost hyperparameters. Defaults to a basic config.
        num_rounds (int, optional): Number of boosting rounds (n_estimators). Default is 100.
        model_path (str, optional): File path to save the trained model (joblib). If None, model is not saved.

    Returns:
        xgb.XGBClassifier: Trained XGBoost model.
    """
    # Default hyperparameters
    default_params = {
        "n_estimators": num_rounds,
        "max_depth": 3,
        "learning_rate": 0.1,
        "use_label_encoder": False,
        "eval_metric": "logloss"
    }
    if params:
        default_params.update(params)
    
    # Initialize and train
    model = xgb.XGBClassifier(**default_params)
    model.fit(X_train, y_train)

    # Save model if path provided
    if model_path:
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        joblib.dump(model, model_path)

    return model


def evaluate_model(model: xgb.XGBClassifier,
                   X_test: pd.DataFrame,
                   y_test: pd.Series,
                   show_report: bool = True) -> dict:
    """
    Evaluate a trained classifier on test data and return key metrics.

    Args:
        model (xgb.XGBClassifier): Trained model.
        X_test (pd.DataFrame): Feature matrix for testing.
        y_test (pd.Series): True labels for testing.
        show_report (bool, optional): If True, print classification report and confusion matrix.

    Returns:
        dict: Dictionary containing accuracy, precision, recall, f1-score.
    """
    # Predict
    y_pred = model.predict(X_test)

    # Compute metrics
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred, zero_division=0),
        "recall": recall_score(y_test, y_pred, zero_division=0),
        "f1_score": f1_score(y_test, y_pred, zero_division=0)
    }

    if show_report:
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, zero_division=0))
        print("Confusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    return metrics
