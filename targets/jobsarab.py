from bs4 import BeautifulSoup
from targets.base import get_target
from typing import List,Dict

#TODO add filters
LINKS = ["https://www.jobs-arab.com/sa/job-location/%d8%ac%d8%af%d9%87/"]

def update_jobs() -> List[Dict[str,str]]:
    jobs = []
    try:
        for link in LINKS:
            soup = BeautifulSoup(get_target(link).text,"html.parser")
            listed_jobs = soup.find("ul",attrs={"class":"jobs"}).find_all("a")
            for listed_job in listed_jobs:
                job_link = listed_job["href"]
                job_id = job_link.removesuffix("/").split("/")[-1]
                job_title = listed_job.text.replace("مطلوب","").strip()
                
                jobs.append({"job_id":job_id,"provider":"Sabbar","title":job_title,"link":job_link})

        return jobs
    except Exception as e:
        raise Exception(e)
    
def get_description(link : str) -> str:
    soup = BeautifulSoup(get_target(link).text,"html.parser")
    
    desc = soup.find("section",attrs={"class":"job-description"}).p.text.strip()
    
    return desc
