from flask import Flask, request, jsonify
from github_service import evaluate_repo
from model import Model
from data_service import DataService

app = Flask(__name__)
model = Model()
data_service = DataService()

def calculate_score(evaluation, existing_data):
    average_commit_count = existing_data['commit_count'].mean()
    average_code_size = existing_data['code_size_mb'].mean()
    average_duration = existing_data['duration_days'].mean()
    average_open_issues = existing_data['open_issues'].mean()
    average_pull_requests = existing_data['pull_requests'].mean()
    average_forks = existing_data['forks'].mean()

    score = 0
    score += min(evaluation['commit_count'] / average_commit_count, 1) * 30 if average_commit_count > 0 else 0
    score += min(evaluation['code_size_mb'] / average_code_size, 1) * 30 if average_code_size > 0 else 0
    score += min(evaluation['duration_days'] / average_duration, 1) * 40 if average_duration > 0 else 0
    score += min(evaluation['open_issues'] / average_open_issues, 1) * 10 if average_open_issues > 0 else 0
    score += min(evaluation['pull_requests'] / average_pull_requests, 1) * 10 if average_pull_requests > 0 else 0
    score += min(evaluation['forks'] / average_forks, 1) * 10 if average_forks > 0 else 0

    return min(int(score), 100)


@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    username = data.get('username')
    repo_name = data.get('repo_name')

    try:
        evaluation = evaluate_repo(username, repo_name)

        existing_data = data_service.load_data()
        if existing_data.empty:
            evaluation['score'] = 100
        else:
            evaluation['score'] = calculate_score(evaluation, existing_data)

        data_service.save_evaluation(evaluation, model)
        return jsonify(evaluation), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    username = data.get('username')
    repo_name = data.get('repo_name')

    try:
        evaluation = evaluate_repo(username, repo_name)

        predicted_score = model.predict(
            evaluation['commit_count'],
            evaluation['code_size_mb'],
            evaluation['duration_days'],
            evaluation['open_issues'],
            evaluation['pull_requests'],
            evaluation['stars'],
            evaluation['forks'],
            evaluation['branches']
        )

        evaluation['predicted_score'] = predicted_score
        return jsonify(evaluation), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
