def load_data(path):
    df = pd.read_csv(path)
    df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})
    return df

def prepare_splits(df, test_size=0.2):
    X = df.drop('Attrition', axis=1)
    y = df['Attrition']
    return train_test_split(
        X, y, 
        test_size=test_size,
        stratify=y,
        random_state=42)

#%% EXECUTION SCRIPT
if __name__ == "__main__":
    # Load and prepare data
    df = load_data(DATA_RAW)
    X_train, X_test, y_train, y_test = prepare_splits(df)
    
    # Initialize and train pipeline
    pipeline = AttritionPipeline()
    best_params = pipeline.train(X_train, y_train)
    print(f"Best Model Parameters: {best_params}")
    
    # Evaluate performance
    pipeline.evaluate(X_test, y_test)
    
    # Save model artifact
    pipeline.save_model(MODEL_DIR / "attrition_model_v1.pkl")