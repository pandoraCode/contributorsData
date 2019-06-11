import requests
import json
import github3
import csv
from github import Github
from slugify import slugify


repos= []
users= []
tokens = []

g = Github("")


#connect to githubApi
def connect_to_github(token):
    g= Github(token)


#to return new repo object
def get_repo(repo):
    return g.get_repo(repo)



#get needed info Shawn Allen
def get_contributors_info(repo):
    repo = get_repo(repo)
    for c in repo.get_contributors():
        numCommits = repo.get_commits(author=c).totalCount
        numIssues= repo.get_issues(creator=c).totalCount
        if c.email:
            print([repo.name,c.name,c.email,numCommits,numIssues,c.company,c.location,c.bio])
            users.append([repo.name,c.name,c.email,numCommits,numIssues,c.company,c.location,c.bio])
    print(repo.name , " finished")


#parse  info to csv file
def parse_userInfo(repo):
    filename= "alali/%s.csv" % slugify(repo)
    

    with open(filename, 'w+') as f:
     wr = csv.writer(f, quoting=csv.QUOTE_ALL)
     for row in users:
         wr.writerow(row)
    f.close()
    users.clear()
    print(repo," user info file was generated successfully")

#get all repos from csv and store them in repos' list
def get_repos():
    with open('repos.csv', 'r') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            repos.append([row[0]])
    csvFile.close()




#test the repos connection

def test_connection(repo):
    try: 
        g.get_repo(repo)
        return 1
    except:
        return 0


#main function

def main():
    get_repos()
    for repo in repos:
        print(repo[0])
        if test_connection(repo[0]):
            get_contributors_info(repo[0])
            parse_userInfo(repo[0])
            



if __name__ == '__main__':
    main()
