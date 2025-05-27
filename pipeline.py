import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score
import joblib

class AttritionPipeline:
    def __init__(self):
        self.numeric_features = ['Age', 'DailyRate', 'DistanceFromHome', 
                                'MonthlyIncome', 'YearsAtCompany']
        self.categorical_features = ['Department', 'EducationField', 
                                   'JobRole', 'OverTime']
        self.target = 'Attrition'
        
        self.preprocessor = self._create_preprocessor()
        self.model = self._create_model()
        self.pipeline = Pipeline([
            ('preprocessor', self.preprocessor),
            ('classifier', self.model)
        ])
    
    def _create_preprocessor(self):
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])
        
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])
        
        return ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numeric_features),
                ('cat', categorical_transformer, self.categorical_features)])
    
    def _create_model(self):
        return RandomForestClassifier(
            class_weight='balanced',
            random_state=42,
            n_jobs=-1)
    
    def train(self, X, y):
        param_grid = {
            'classifier__n_estimators': [100, 200],
            'classifier__max_depth': [None, 10],
            'classifier__min_samples_split': [2, 5]}
        
        search = GridSearchCV(
            self.pipeline,
            param_grid,
            cv=5,
            scoring='roc_auc',
            verbose=1)
        
        search.fit(X, y)
        self.pipeline = search.best_estimator_
        return search.best_params_
    
    def evaluate(self, X_test, y_test):
        y_pred = self.pipeline.predict(X_test)
        y_proba = self.pipeline.predict_proba(X_test)[:,1]
        
        print(classification_report(y_test, y_pred))
        print(f"ROC AUC: {roc_auc_score(y_test, y_proba):.3f}")
    
    def save_model(self, path):
        joblib.dump(self.pipeline, path)
    
    @staticmethod
    def load_model(path):
        return joblib.load(path)