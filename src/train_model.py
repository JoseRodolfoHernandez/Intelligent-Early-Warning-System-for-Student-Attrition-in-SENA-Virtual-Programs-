import pandas as pd
import joblib # Para guardar el modelo
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

def train_attrition_model(data_path):
    print(f"--- Training Model with {data_path} ---")
    df = pd.read_csv(data_path)

    # 1. Prepare the variables (X) and the target (y)
    # We convert categories (text) to numbers (One-Hot Encoding)
    X = df.drop('ATTRITION_RATE', axis=1)
    X = pd.get_dummies(X, columns=['NOMBRE_REGIONAL', 'NIVEL_FORMACION'])
    y = df['ATTRITION_RATE']

    # 2. Split data: 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 3. Create and train the model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 4. Evaluation (Phase 4 of CRISP-ML)
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)

    print(f"--- Evaluation Results ---")
    print(f"Mean Absolute Error: {mae:.4f}")
    print(f"R-squared Score: {r2:.4f}")

    # 5. Save the model and columns for future use
    joblib.dump(model, 'src/attrition_model.pkl')
    joblib.dump(X.columns.tolist(), 'src/model_columns.pkl')
    print("--- Model saved as attrition_model.pkl ---")

if __name__ == "__main__":
    train_attrition_model('data/sena_virtual_cleaned.csv')