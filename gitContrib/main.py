import requests, json
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from datetime import datetime, timedelta

# Load secrets from the JSON file
with open('secrets.json') as f:
    secrets = json.load(f)

# Assign secrets to variables
GITHUB_API_URL = secrets['GITHUB_API_URL']
GITLAB_API_URL = secrets['GITLAB_API_URL']
GITLAB_AUTH_TOKEN = secrets['GITLAB_AUTH_TOKEN']

# Function to fetch GitHub contributions
def fetch_github_contributions(username):
    response = requests.get(GITHUB_API_URL.format(username=username))
    events = response.json()
    contributions = {}
    for event in events:
        date = event['created_at'][:10]
        contributions[date] = contributions.get(date, 0) + 1
    return contributions

# Function to fetch GitLab contributions from a local instance
def fetch_gitlab_contributions(user_id):
    headers = {'PRIVATE-TOKEN': GITLAB_AUTH_TOKEN}
    response = requests.get(GITLAB_API_URL.format(user_id=user_id), headers=headers)
    events = response.json()
    contributions = {}
    for event in events:
        date = event['created_at'][:10]
        if event.get('push_data') and event['push_data'].get('commit_count'):
            commit_count = event['push_data']['commit_count']
        else:
            commit_count = 1
        contributions[date] = contributions.get(date, 0) + commit_count
    return contributions

# Combine contributions
def combine_contributions(github_contributions, gitlab_contributions):
    combined = {}
    all_dates = set(github_contributions.keys()).union(set(gitlab_contributions.keys()))
    for date in all_dates:
        combined[date] = github_contributions.get(date, 0) + gitlab_contributions.get(date, 0)
    return combined

# Generate the heatmap
def generate_heatmap(contributions, image_path):
    dates = pd.date_range(start=min(contributions.keys()), end=max(contributions.keys()))
    data = pd.DataFrame(index=dates)
    data['count'] = 0

    for date, count in contributions.items():
        data.loc[date, 'count'] = count

    data['weekday'] = data.index.weekday
    data['week'] = data.index.to_period('W').strftime('%Y-%m-%d')

    pivot_table = data.pivot(index='weekday', columns='week', values='count')

    fig, ax = plt.subplots(figsize=(20, 6))
    cax = ax.matshow(pivot_table, cmap='Greens', aspect='auto')
    plt.colorbar(cax)

    ax.set_xticks(range(len(pivot_table.columns)))
    month_names = [pd.to_datetime(date).strftime('%b') for date in pivot_table.columns]
    ax.set_xticklabels(month_names, rotation=90)
    ax.set_yticks(range(7))
    ax.set_yticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

    # Save the figure
    plt.savefig(image_path)
    plt.show()


# Fetch contributions
github_contributions = fetch_github_contributions('caggursoy')
gitlab_contributions = fetch_gitlab_contributions('65')

# Combine contributions
combined_contributions = combine_contributions(github_contributions, gitlab_contributions)

# Generate heatmap and save as image
generate_heatmap(combined_contributions, 'contributions_heatmap.png')

# Create README.md file with the image
readme_content = """
# Contributions Heatmap

This heatmap shows the combined contributions from GitHub and GitLab.

![Contributions Heatmap](contributions_heatmap.png)
"""

with open('README.md', 'w') as readme_file:
    readme_file.write(readme_content)