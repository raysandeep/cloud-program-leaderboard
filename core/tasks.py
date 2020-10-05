from django.conf import settings
from core.models import UserModel
import requests 
from bs4 import BeautifulSoup
from celery import shared_task 

CHALLENGES_AVAILABLE = [
    'Integrate with Machine Learning APIs', 
    'Perform Foundational Data, ML, and AI Tasks in Google Cloud', 
    'Explore Machine Learning Models with Explainable AI', 
    'Engineer Data in Google Cloud', 
    'Insights from Data with BigQuery', 
    'Deploy to Kubernetes in Google Cloud', 
    'Build and Secure Networks in Google Cloud', 
    'Deploy and Manage Cloud Environments with Google Cloud', 
    'Set up and Configure a Cloud Environment in Google Cloud', 
    'Perform Foundational Infrastructure Tasks in Google Cloud', 
    'Getting Started: Create and Manage Cloud Resources',
    'Google Cloud Essentials'
    ]



URL = "https://google.qwiklabs.com/public_profiles/7e0abd7b-15e0-4e51-8db2-1d552322ad3c"
def GetCountAndResourcesDone(URL):
    COMPLETED_QUESTS = []
    r = requests.get(URL) 
    soup = BeautifulSoup(r.content, 'html5lib')
    quests = soup.findAll('div', attrs = {'class':'public-profile__badges'})   
    for row in quests[0].findAll('div', attrs = {'class':'public-profile__badge'}): 
        divs = row.findChildren("div" , recursive=False)
        if divs[1].text.strip() in CHALLENGES_AVAILABLE:
            COMPLETED_QUESTS.append(divs[1].text.strip())
    profile = soup.findAll('div', attrs = {'class':'public-profile__hero'})[0]
    dp = profile.img['src']
    name = profile.h1.text
    return {
        "quests":COMPLETED_QUESTS,
        "dp":dp,
        "name":name.strip()
    }



@shared_task
def summary():
    print("Starting scrap")
    users = UserModel.objects.all()
    for  i in range(users.count()):
        user = users[i]
        data = GetCountAndResourcesDone(user.qwiklabs_id)   
        user.quests_status = len(data['quests'])
        user.quests = data['quests']
        user.save()
        print(i)
