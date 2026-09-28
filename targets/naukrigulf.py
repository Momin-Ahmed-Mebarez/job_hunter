#NOTE The results from this site are unordered by nature, I am trying to get the latest while respecting not to pull the entire site listed jobs

from bs4 import BeautifulSoup
#from targets.base import get_target
from base import get_target
from typing import List,Dict

#TODO add filters
LINKS = ["https://www.gulftalent.com/api/jobs/search?config%5Bfilters%5D=DISABLED&config%5BisDynamicSearchV2%5D=true&filters%5Bcity%5D[0]=10111112000122&filters%5Bcountry%5D[0]=10111112000000&include_scraped=1&limit=300&offset=0&search_keyword=&search_order=d&version=2"]
SITE = "https://www.gulftalent.com"


def update_jobs() -> List[Dict[str,str]]:
    jobs = []
    try:
        for link in LINKS:
            #Returns the most recent 18 job advertisment (The first site I used only shows 18 job on the home page that is why I am using 18 but it doesn't matter)
            listed_jobs = sorted(get_target(link).json()["results"]["data"],key=lambda k: k["posted_date_ts"],reverse=True)[:18]
            for job in listed_jobs:
                job_link = SITE + job["link"]
                job_id = job["id"]
                job_title = job["title"]

                jobs.append({"job_id":job_id,"provider":"Naukrigulf","title":job_title,"link":job_link})
        return jobs
    except Exception as e:
        raise Exception(e)

def get_description(link : str) -> str:
    soup = BeautifulSoup(get_target(link).text,"html.parser")
    
    desc_div = soup.find("div",attrs={"class":"panel-body"})
    desc = desc_div.get_text("\n",strip=True)
    
    return desc
