import pandas as pd
import numpy as np
import pickle
import os
from sklearn.linear_model import LinearRegression

class Model:
    def __init__(self):
        self.model = LinearRegression()
        self.data_file = 'repo_data.csv'
        self.load_model()

    def load_model(self):
        if os.path.exists('model.pkl'):
            with open('model.pkl', 'rb') as f:
                self.model = pickle.load(f)

    def save_model(self):
        with open('model.pkl', 'wb') as f:
            pickle.dump(self.model, f)

    def train(self, new_data):
        existing_data = self.load_data()
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)

        if combined_data.isnull().values.any():
            print("Need to clean yor data.")
            return
        
        self.save_data(combined_data)

        X = combined_data[['commit_count', 'code_size_mb', 'duration_days', 'open_issues', 'pull_requests', 'stars', 'forks', 'branches']]
        y = combined_data['score']
        self.model.fit(X, y)
        self.save_model()

    def predict(self, commit_count, code_size_mb, duration_days, open_issues, pull_requests, stars, forks, branches):
        return int(self.model.predict(np.array([[commit_count, code_size_mb, duration_days, open_issues, pull_requests, stars, forks, branches]]))[0])

    def load_data(self):
        if os.path.exists(self.data_file):
            return pd.read_csv(self.data_file)
        return pd.DataFrame(columns=['commit_count', 'code_size_mb', 'duration_days', 'score', 'open_issues', 'pull_requests', 'stars', 'forks', 'branches'])

    def save_data(self, data):
        data.to_csv(self.data_file, index=False)

    def info(self):
        return {
            'model_coefficients': self.model.coef_.tolist(),
            'model_intercept': self.model.intercept_
        }
