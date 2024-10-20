import pandas as pd
import os

class DataService:
    def __init__(self, filename='repo_data.csv'):
        self.data_file = filename

    def load_data(self):
        if os.path.exists(self.data_file):
            return pd.read_csv(self.data_file)
        return pd.DataFrame(columns=['commit_count', 'code_size_mb', 'duration_days', 'score', 'open_issues', 'pull_requests', 'stars', 'forks', 'branches'])

    def save_data(self, data):
        data.to_csv(self.data_file, index=False)

    def save_evaluation(self, evaluation, model_instance):
        new_data = pd.DataFrame({
            'commit_count': [evaluation['commit_count']],
            'code_size_mb': [evaluation['code_size_mb']],
            'duration_days': [evaluation['duration_days']],
            'score': [evaluation['score']],
            'open_issues': [evaluation['open_issues']],
            'pull_requests': [evaluation['pull_requests']],
            'stars': [evaluation['stars']],
            'forks': [evaluation['forks']],
            'branches': [evaluation['branches']],
        })
        
        model_instance.train(new_data)
