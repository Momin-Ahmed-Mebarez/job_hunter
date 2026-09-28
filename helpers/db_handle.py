from typing import Dict,Any,List
from pathlib import Path
import traceback
import sqlite3

class DBHandle():
    HOME = Path(__file__).resolve().parent

    def __init__(self,connection : sqlite3.Connection):
        self.connection = connection

    def init_db(self) -> None:
        with open(self.HOME / "schema.sql","r") as f:
            script = f.read()
        self.connection.executescript(script)

    def drop_tables(self) -> None:
        self.connection.execute("DROP TABLE jobs")

    def add_job(self, job : Dict[str,Any]):
        job["title"] = job["title"] if job.get("title") != None else "no_title_available"
        #job["description"] = job["description"] if job.get("description") != None else "no_description_available"
        job["description"] = "" #We avoid saving the job description as it might be looked upon as copyright infringement

        try:
            self.connection.execute("INSERT OR IGNORE into jobs (job_id,provider,title,description,link,showable) values (:job_id,:provider,:title,:description,:link,:showable)",job)
        except Exception as e:
            #print(traceback.format_exc())
            self.connection.rollback()
            raise Exception("Couldn't write job to database (this shouldn't happen)") from e
        
        self.connection.commit()

    def read_jobs(self) -> List[Dict[str,Any]]:
        cursor = self.connection.execute("SELECT * FROM jobs WHERE applied = 0 AND showable = 1 ORDER BY date DESC limit 100")
        return [dict(row) for row in cursor.fetchall()]
    
    def check_job_exists(self,filter: Dict[str,str]) -> bool:
        cursor = self.connection.execute("SELECT 1 FROM jobs WHERE job_id = :job_id AND provider = :provider",filter)
        return cursor.fetchone() != None

    def change_apply_to_true(self,filter: Dict[str,str]) -> None:
        try:
            self.connection.execute("UPDATE jobs SET applied = 1 WHERE job_id = :job_id AND provider = :provider",filter)
        except Exception as e:
            self.connection.rollback()
            raise Exception("An error Occurred while changing to applied") from e
        
        self.connection.commit()
        return None