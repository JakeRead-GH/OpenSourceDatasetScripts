from github import Github, GithubException
import pandas as pd

#Connecting to GitHub account using personal access key
token_file = open("github_access_token.txt")
ACCESS_TOKEN = token_file.readline()
token_file.close()

g = Github(ACCESS_TOKEN)


#Pulling "Repo Link" collumn from dataset
apps = pd.read_excel("dataset.xlsx")
repo_links = apps["Repo Link"]


#Main Program
output = open("last_commits.txt", 'w')

for repo_link in repo_links:
    repo_id = repo_link.replace("https://github.com/", '')

    try:        
        repo = g.get_repo(repo_id)
        commits = repo.get_commits()
        
        latest_commit = str(commits[0].commit.committer.date)
        latest_commit_formatted = latest_commit.split(" ")[0]
        
        output.write(latest_commit_formatted + '\n')
        
    except GithubException:
        output.write("Couldn't find repo, enter date manually\n")
    
output.close()
