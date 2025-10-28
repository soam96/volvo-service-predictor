import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os

class VolvoServicePredictor:
    def __init__(self):
        self.model = None
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = []
        
    def load_and_explore_data(self, data_path):
        """Load and explore the dataset"""
        print("📊 Loading dataset...")
        df = pd.read_csv(data_path)
        
        print(f"Dataset Shape: {df.shape}")
        print(f"\nDataset Info:")
        print(df.info())
        
        print(f"\nFirst 5 rows:")
        print(df.head())
        
        print(f"\nMissing values:")
        print(df.isnull().sum())
        
        print(f"\nBasic statistics:")
        print(df.describe())
        
        return df
    
    def preprocess_data(self, df):
        """Preprocess the dataset for training"""
        print("🔄 Preprocessing data...")
        df_processed = df.copy()
        
        # Encode categorical variables
        categorical_columns = ['Car_Model', 'Fuel_Type', 'Service_Type', 'Parts_Availability']
        
        for col in categorical_columns:
            self.label_encoders[col] = LabelEncoder()
            df_processed[col] = self.label_encoders[col].fit_transform(df_processed[col])
            print(f"Encoded {col}: {len(self.label_encoders[col].classes_)} categories")
            print(f"  Categories: {list(self.label_encoders[col].classes_)}")
        
        # Define feature columns
        self.feature_columns = [col for col in df_processed.columns if col != 'Service_Time_Hours']
        
        print(f"Feature columns: {self.feature_columns}")
        print(f"Target column: Service_Time_Hours")
        
        return df_processed
    
    def analyze_features(self, df):
        """Analyze feature importance and correlations"""
        print("📈 Analyzing features...")
        
        # Create a copy for analysis with encoded categoricals
        df_encoded = df.copy()
        
        # Encode categorical variables for analysis only
        categorical_columns = ['Car_Model', 'Fuel_Type', 'Service_Type', 'Parts_Availability']
        for col in categorical_columns:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col])
        
        # Correlation matrix
        plt.figure(figsize=(12, 8))
        correlation_matrix = df_encoded.corr()
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, fmt='.2f')
        plt.title('Feature Correlation Matrix')
        plt.tight_layout()
        
        # Create models directory if it doesn't exist
        os.makedirs('models', exist_ok=True)
        plt.savefig('models/feature_correlation.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Target variable distribution
        plt.figure(figsize=(10, 6))
        plt.hist(df['Service_Time_Hours'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        plt.xlabel('Service Time (Hours)')
        plt.ylabel('Frequency')
        plt.title('Distribution of Service Time')
        plt.grid(True, alpha=0.3)
        plt.savefig('models/service_time_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Categorical variable distributions
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        axes = axes.ravel()
        
        categorical_cols = ['Car_Model', 'Fuel_Type', 'Service_Type', 'Parts_Availability']
        for i, col in enumerate(categorical_cols):
            df[col].value_counts().plot(kind='bar', ax=axes[i], color='lightblue')
            axes[i].set_title(f'Distribution of {col}')
            axes[i].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('models/categorical_distributions.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Feature analysis completed and plots saved")
    
    def train_model(self, df, test_size=0.2, random_state=42):
        """Train XGBoost model with comprehensive evaluation"""
        print("🎯 Training XGBoost model...")
        
        # Preprocess data
        df_processed = self.preprocess_data(df)
        
        # Prepare features and target
        X = df_processed[self.feature_columns]
        y = df_processed['Service_Time_Hours']
        
        print(f"X shape: {X.shape}, y shape: {y.shape}")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, shuffle=True
        )
        
        print(f"Training set: {X_train.shape[0]} samples")
        print(f"Testing set: {X_test.shape[0]} samples")
        
        # Scale numerical features
        numerical_cols = ['Manufacture_Year', 'Last_Service_Days_Ago', 'Total_Kms', 
                         'Km_From_Last_Service', 'Worker_Availability', 'No_Of_Tasks']
        
        X_train[numerical_cols] = self.scaler.fit_transform(X_train[numerical_cols])
        X_test[numerical_cols] = self.scaler.transform(X_test[numerical_cols])
        
        # Train XGBoost model with hyperparameters
        self.model = xgb.XGBRegressor(
            n_estimators=1000,
            learning_rate=0.1,
            max_depth=6,
            min_child_weight=1,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1,
            random_state=random_state,
            n_jobs=-1,
            eval_metric='rmse'
        )
        
        print("🚀 Starting model training...")
        self.model.fit(
            X_train, y_train,
            eval_set=[(X_test, y_test)],
            early_stopping_rounds=50,
            verbose=50
        )
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        
        # Calculate metrics
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print("\n" + "="*50)
        print("📊 MODEL EVALUATION RESULTS")
        print("="*50)
        print(f"R² Score: {r2:.4f}")
        print(f"Mean Absolute Error (MAE): {mae:.4f} hours")
        print(f"Root Mean Squared Error (RMSE): {rmse:.4f} hours")
        print("="*50)
        
        # Feature importance
        self.plot_feature_importance()
        
        # Prediction visualization
        self.plot_predictions(y_test, y_pred)
        
        return X_train, X_test, y_train, y_test, y_pred
    
    def plot_feature_importance(self):
        """Plot feature importance"""
        print("📊 Plotting feature importance...")
        
        feature_importance = self.model.feature_importances_
        indices = np.argsort(feature_importance)[::-1]
        
        plt.figure(figsize=(12, 8))
        plt.title('Feature Importance - XGBoost')
        bars = plt.bar(range(len(feature_importance)), feature_importance[indices], color='steelblue')
        plt.xticks(range(len(feature_importance)), [self.feature_columns[i] for i in indices], rotation=45)
        plt.xlabel('Features')
        plt.ylabel('Importance')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.3f}',
                    ha='center', va='bottom', rotation=0)
        
        plt.tight_layout()
        plt.savefig('models/feature_importance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Feature importance plot saved")
    
    def plot_predictions(self, y_true, y_pred):
        """Plot actual vs predicted values"""
        print("📈 Plotting predictions...")
        
        plt.figure(figsize=(15, 10))
        
        plt.subplot(2, 2, 1)
        plt.scatter(y_true, y_pred, alpha=0.6, color='blue')
        plt.plot([y_true.min(), y_true.max()], [y_true.min(), y_true.max()], 'r--', lw=2)
        plt.xlabel('Actual Service Time (Hours)')
        plt.ylabel('Predicted Service Time (Hours)')
        plt.title('Actual vs Predicted')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 2)
        residuals = y_true - y_pred
        plt.scatter(y_pred, residuals, alpha=0.6, color='green')
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel('Predicted Values')
        plt.ylabel('Residuals')
        plt.title('Residual Plot')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 3)
        plt.hist(residuals, bins=50, alpha=0.7, color='orange', edgecolor='black')
        plt.xlabel('Residuals')
        plt.ylabel('Frequency')
        plt.title('Residual Distribution')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(2, 2, 4)
        error_percentage = np.abs(residuals / y_true) * 100
        plt.hist(error_percentage, bins=50, alpha=0.7, color='purple', edgecolor='black')
        plt.xlabel('Absolute Error Percentage (%)')
        plt.ylabel('Frequency')
        plt.title('Prediction Error Distribution')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('models/prediction_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Prediction analysis plots saved")
    
    def save_model(self, file_path='models/volvo_service_predictor.pkl'):
        """Save the trained model and preprocessing objects"""
        print("💾 Saving model...")
        
        model_data = {
            'model': self.model,
            'label_encoders': self.label_encoders,
            'scaler': self.scaler,
            'feature_columns': self.feature_columns,
            'metadata': {
                'training_date': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                'model_type': 'XGBoost',
                'version': '1.0.0'
            }
        }
        
        joblib.dump(model_data, file_path)
        print(f"✅ Model saved to {file_path}")
    
    def load_model(self, file_path='models/volvo_service_predictor.pkl'):
        """Load the trained model and preprocessing objects"""
        print("📥 Loading model...")
        
        model_data = joblib.load(file_path)
        self.model = model_data['model']
        self.label_encoders = model_data['label_encoders']
        self.scaler = model_data['scaler']
        self.feature_columns = model_data['feature_columns']
        
        print("✅ Model loaded successfully")
        return self
    
    def predict_service_time(self, input_features):
        """Predict service time for new input"""
        if self.model is None:
            raise ValueError("Model not trained or loaded yet!")
        
        # Create feature vector
        feature_vector = []
        for col in self.feature_columns:
            if col in ['Car_Model', 'Fuel_Type', 'Service_Type', 'Parts_Availability']:
                # Encode categorical features
                if input_features[col] in self.label_encoders[col].classes_:
                    encoded_value = self.label_encoders[col].transform([input_features[col]])[0]
                    feature_vector.append(encoded_value)
                else:
                    # Handle unseen categories - use most common category
                    print(f"Warning: Unknown category '{input_features[col]}' for {col}")
                    feature_vector.append(0)  # Default to first category
            else:
                feature_vector.append(input_features[col])
        
        # Convert to array and scale numerical features
        feature_array = np.array(feature_vector).reshape(1, -1)
        
        numerical_cols = ['Manufacture_Year', 'Last_Service_Days_Ago', 'Total_Kms', 
                         'Km_From_Last_Service', 'Worker_Availability', 'No_Of_Tasks']
        numerical_indices = [self.feature_columns.index(col) for col in numerical_cols]
        
        feature_array[0, numerical_indices] = self.scaler.transform(
            feature_array[0, numerical_indices].reshape(1, -1))
        
        # Predict
        prediction = self.model.predict(feature_array)[0]
        
        return max(0, prediction)  # Ensure non-negative prediction

def main():
    """Main function to train and save the model"""
    print("🚗 Volvo Service Time Prediction Model Training")
    print("="*60)
    
    # Initialize predictor
    predictor = VolvoServicePredictor()
    
    try:
        # Load data
        df = predictor.load_and_explore_data('data/volvo_service_time_india_10k.csv')
        
        # Analyze features (fixed version)
        predictor.analyze_features(df)
        
        # Train model
        X_train, X_test, y_train, y_test, y_pred = predictor.train_model(df)
        
        # Save model
        predictor.save_model('models/volvo_service_predictor.pkl')
        
        # Test prediction with sample data
        print("\n🧪 Testing prediction with sample data...")
        sample_input = {
            'Car_Model': 'XC60',
            'Manufacture_Year': 2020,
            'Fuel_Type': 'Petrol',
            'Service_Type': 'General Service',
            'Last_Service_Days_Ago': 100,
            'Total_Kms': 50000,
            'Km_From_Last_Service': 5000,
            'Parts_Availability': 'High',
            'Worker_Availability': 15,
            'No_Of_Tasks': 3
        }
        
        predicted_time = predictor.predict_service_time(sample_input)
        print(f"Sample prediction: {predicted_time:.2f} hours")
        
        # Show model performance summary
        print("\n📋 MODEL PERFORMANCE SUMMARY")
        print("="*40)
        print(f"✅ Model trained successfully!")
        print(f"📁 Model saved to: models/volvo_service_predictor.pkl")
        print(f"📊 Analysis plots saved to models/ directory")
        print(f"🔮 Sample prediction: {predicted_time:.2f} hours")
        print("="*40)
        
        print("\n🎉 Model training completed successfully!")
        print("📁 Check the 'models' folder for analysis plots and saved model")
        
    except Exception as e:
        print(f"❌ Error during training: {str(e)}")
        import traceback
        traceback.print_exc()
        raise

if __name__ == '__main__':
    main()