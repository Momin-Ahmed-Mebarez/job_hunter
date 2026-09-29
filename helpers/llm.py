import requests
from pathlib import Path
import time
HOME = Path(__name__).resolve().parent

class LLM():
    header = {"Authorization": ""}
    
    body =  {"model":"",
            "messages":[{"role":"system", "content": ""}] + [{"role":"user", "content": ""}],
            "reasoning_effort": "medium",
            "stream": False,
            "temperature": 0.1,    #Groq temperature support 
            #"keep_alive": 0  #Causes an error if used with groq
            }
    
    def __init__(self):
        self.prompt = ""

    def create_cv_rules(self, msg : str ,llm_link : str,llm_model : str, llm_api : str | None = None):
        self.add_api_key(llm_api)
        self.body["model"] = llm_model
        
        try:
            with open(HOME / "prompts" / "cv_extract_rules.txt") as f:
               self.body["messages"][0]["content"] = f.read().strip()
            resp = self.send_to_llm(msg,llm_link)
            
            if(not resp): raise Exception("THE MODEL COULDN'T GENERATE A RESPONSE")

            with open(HOME / "prompts" / "rules_structure.txt", "r", encoding="utf-8") as f:
                rules_structure = f.read() 

            with open(HOME / "prompts" / "cv_rules.txt", "w", encoding="utf-8") as f:
                f.write(rules_structure + resp)

        except Exception as e:
            raise e
        
    #Checks if the job suitable 
    def check_suitable(self, msg : str ,llm_link : str,llm_model : str, llm_api : str | None = None) -> bool:
        self.add_api_key(llm_api)
        self.body["model"] = llm_model
        try:
            if(not self.prompt): self.load_prompt()

            self.body["messages"][0]["content"] = self.prompt
            resp = self.send_to_llm(msg,llm_link)
            
            if(not resp): raise Exception("THE MODEL COULDN'T GENERATE A RESPONSE")
            print("LLM resp is: " + resp)
            return resp.strip().upper() in ("UNCERTAIN", "SUITABLE") or resp.strip().upper() not in ("NOT_SUITABLE")
        
        except Exception as e:
            raise e

    def send_to_llm(self,msg : str,llm_link : str) -> str | None:
        self.body["messages"][1]["content"] = msg
        try:
            resp = requests.post(llm_link,headers=self.header,json=self.body).json()
            time.sleep(5) #Can be disabled for local models, I added it to protect external api's
        
            resp = resp["choices"][0]["message"]["content"]
            return resp
        except requests.exceptions.Timeout:
            raise Exception("The model timed out, choice a faster model or change the prompt")
        except Exception as e:
            raise Exception("An error occured while trying to generate a response: " + str(e))            

    def load_prompt(self):
        with open(HOME / "prompts" / "cv_rules.txt", "r", encoding="utf-8") as f:
            self.prompt = f.read()

    def add_api_key(self,api_key : str):
        if(api_key):
            self.header["Authorization"] = "Bearer " + api_key.strip()
        else:
             self.header["Authorization"] = ""

