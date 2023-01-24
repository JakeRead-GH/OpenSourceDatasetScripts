#!/usr/bin/env python
# coding: utf-8


import time
from dotenv import load_dotenv
import os
from typing import Final

GITHUB_ACCESS_TOKEN: Final[str] = os.environ.get("token")


import pandas as pd
apps = pd.read_excel("dataset.xlsx")
repoList = apps["Repo Link"]
repoList = repoList.str.replace('https://github.com/','')
repoList


from github import Github, GithubException
import time

github = Github(GITHUB_ACCESS_TOKEN)


from github.ContentFile import ContentFile
from logger import logging
from typing import Iterable
from pyjavaproperties import Properties
from io import StringIO
p = Properties()

for i, repo_id in repoList.items():
    repo = github.get_repo(repo_id)
    files = repo.get_contents("")
    if isinstance(files, Iterable):
        files_s = [str(f.name) for f in files]
    else:
        files_s = []
    manifest = ""
    apps.at[i, "mod"] = repo.last_modified
    apps.at[i, "gradle"] = "gradle" in files_s
    apps.at[i, "gradlew"] = "gradlew" in files_s
    if "gradle" in files_s:
        try:
            repo_file_content = repo.get_contents("app/src/main/AndroidManifest.xml")
            gradlew_ver = repo.get_contents("gradle/wrapper/gradle-wrapper.properties")
            if isinstance(repo_file_content, ContentFile):
                manifest = repo_file_content.decoded_content.decode()
            if isinstance(gradlew_ver, ContentFile):
                wr_prop = gradlew_ver.decoded_content.decode()
                with StringIO(wr_prop) as f:
                    p.load(f)

        except GithubException as e:
            print(repo_id)
            logging.error(e)
    apps.at[i, "manifest"] = manifest
    apps.at[i, "grv"] = p["distributionUrl"]
    time.sleep(0.5)


apps["mod"] = apps["mod"].apply(lambda a: pd.to_datetime(a).date())
autogradle = apps[(apps["gradlew"]==True) & (apps["manifest"]!="")]
df = autogradle.sort_values(by="mod")


df


df.to_excel("output.xlsx")




