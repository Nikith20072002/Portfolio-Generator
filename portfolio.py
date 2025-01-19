import os
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Your GitHub username
GITHUB_USERNAME = "your_github_username"

# Function to fetch repositories from GitHub
def fetch_github_repos(username):
    url = f"https://api.github.com/users/Nikith20072002/repos"
    response = requests.get(url)
    if response.status_code == 200:
        repos = response.json()
        # Filter repositories (optional)
        return [
            {
                "name": repo["name"],
                "html_url": repo["html_url"],
                "description": repo["description"],
                "language": repo["language"],
            }
            for repo in repos
        ]
    else:
        print(f"Error: Unable to fetch repositories (Status code: {response.status_code})")
        return []

@app.route("/")
def portfolio():
    repos = fetch_github_repos(GITHUB_USERNAME)
    return render_template("portfolio.html", repos=repos)

if __name__ == "__main__":
    # Ensure templates folder exists with portfolio.html
    if not os.path.exists("templates"):
        os.makedirs("templates")
    
    # Create a basic HTML template for the portfolio
    portfolio_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ GITHUB_USERNAME }}'s GitHub Portfolio</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            padding: 20px;
            background-color: #f4f4f4;
        }
        .repo {
            background: #fff;
            margin: 20px 0;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .repo a {
            color: #0366d6;
            text-decoration: none;
        }
        .repo a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>{{ GITHUB_USERNAME }}'s GitHub Portfolio</h1>
    {% for repo in repos %}
    <div class="repo">
        <h2><a href="{{ repo.html_url }}" target="_blank">{{ repo.name }}</a></h2>
        <p>{{ repo.description or "No description available" }}</p>
        <p><strong>Language:</strong> {{ repo.language or "Not specified" }}</p>
    </div>
    {% endfor %}
</body>
</html>
"""
    with open("templates/portfolio.html", "w") as f:
        f.write(portfolio_html)

    app.run(debug=True)

