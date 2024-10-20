# GitHub Repository Evaluator

This project allows you to evaluate GitHub repositories based on various metrics, such as the number of commits, code size, duration of the repository's existence, and other parameters. The evaluation is performed using a linear regression model that is trained on the collected data.

## Features

- Evaluate a repository based on the following parameters:
  - Number of commits
  - Code size (in MB)
  - Duration of the repository's existence (in days)
  - Number of open issues
  - Number of pull requests
  - Number of stars
  - Number of forks
  - Number of branches
- Train the model based on the collected data
- Support for environment variables for confidential information (GitHub token)

## Project Structure

```
.
├── app.py
├── data_service.py
├── github_service.py
├── model.py
├── repo_data.csv
├── requirements.txt
└── .env
```

## Installation

1. Clone the repository:

   `git clone https://github.com/timkmit/repo-evaluate`
   `cd repo-evaluate`

2. Install the required dependencies:

   `pip install -r requirements.txt`

3. Create a `.env` file in the root directory of the project and add your GitHub token:

   `GITHUB_TOKEN=your_github_token`

4. Run the application:

   `python app.py`

### Evaluating a Repository

Send a POST request to `/evaluate` with a JSON body containing the username and repository name:

```JSON
{
	"username": "username",
	"repo_name": "repository_name"
}
```

### Prediction

Send a POST request to `/predict` with the same data to obtain the predicted score:

```JSON
{
	"username": "username",
	"repo_name": "repository_name"
}
```
