from bs4 import BeautifulSoup
from targets.base import get_target
from typing import List,Dict

#TODO add filters
LINKS = ["https://sabbar.com/en/jobs/c-jeddah","https://sabbar.com/ar/jobs/c-%D8%AC%D8%AF%D8%A9"]

SITE = "https://sabbar.com"

def update_jobs() -> List[Dict[str,str]]:
    jobs = []
    try:
        for link in LINKS:
            soup = BeautifulSoup(get_target(link),"html.parser")
        
            listed_jobs = soup.find_all("div",attrs={"class":"job-card"})
    
            for listed_job in listed_jobs:
                job_link = SITE + listed_job.a["href"]
                job_id = job_link.replace("id-","").split("/")[-1]
                job_title = listed_job.a["title"]

                jobs.append({"job_id":job_id,"provider":"Sabbar","title":job_title,"link":job_link})
            
        return jobs
    except Exception as e:
        raise Exception(e)