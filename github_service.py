from github import Github
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

g = Github(GITHUB_TOKEN)

def evaluate_repo(username, repo_name):
    repo = g.get_user(username).get_repo(repo_name)
    
    commits = repo.get_commits()
    commit_count = commits.totalCount
    code_size = sum([file.size for file in repo.get_contents("")])
    created_at = repo.created_at

    if commit_count > 0:
        last_commit_date = commits[0].commit.author.date
    else:
        last_commit_date = created_at

    duration = (last_commit_date - created_at).days

    languages = repo.get_languages()
    total_lines = sum(languages.values())
    language_percentages = {lang: (size / total_lines) * 100 for lang, size in languages.items()}

    open_issues = repo.open_issues_count
    pull_requests = repo.get_pulls().totalCount
    stars = repo.stargazers_count
    forks = repo.forks_count
    branches = repo.get_branches().totalCount

    return {
        'commit_count': commit_count,
        'code_size_mb': code_size / (1024 * 1024), 
        'duration_days': duration, 
        'languages': language_percentages,
        'open_issues': open_issues,
        'pull_requests': pull_requests,
        'stars': stars,
        'forks': forks,
        'branches': branches
    }
