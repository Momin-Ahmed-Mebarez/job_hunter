from pathlib import Path
from dotenv import set_key,find_dotenv,load_dotenv

HUNTER_HOME = Path(__file__).resolve().parents[1]

def store_keys(cv_key: str,title_key: str,job_key: str):
    dotenv = find_dotenv(HUNTER_HOME / ".env")
    load_dotenv(dotenv)
    print(cv_key,title_key,job_key)
    set_key(dotenv,key_to_set="cv_llm_api_key",value_to_set=cv_key if cv_key else "")
    set_key(dotenv,key_to_set="title_llm_api_key",value_to_set=title_key if title_key else "")
    set_key(dotenv,key_to_set="job_llm_api_key",value_to_set=job_key if job_key else "" )