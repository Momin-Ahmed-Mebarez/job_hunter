#TODO log unhandeled errors in a file
#TODO automate updating chrome version 
from curl_cffi import requests
from typing import Dict,Any

#Keep chrome version updated for better anit-detection 
basic_header = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        }

def get_target(url : str ,header : Dict[str,Any] = basic_header) -> requests.Response:
    try:
        resp = requests.get(url,headers=header,impersonate="chrome",timeout=8)
        resp.raise_for_status()

        return resp
    
    except requests.exceptions.HTTPError:
        raise Exception(f"Request wasn't succesful Error: {resp.status_code}")
    except requests.exceptions.Timeout:
        raise Exception(f"Request timedout, try again later or chek if site is down")
    except Exception as e:
        #raise Exception(f"Unhandled error occured please submit the full traceback to the creator") from e
        raise Exception(f"Unhandled error occured") from e
