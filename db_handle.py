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

    def add_job(self, job : Dict[str,Any]) -> bool | None:
        job["title"] = job["title"] if job.get("title") != None else "no_title_available"
        job["description"] = job["description"] if job.get("description") != None else "no_description_available"
    
        try:
            cursor = self.connection.execute("INSERT OR IGNORE into jobs (job_id,provider,title,description,link) values (:job_id,:provider,:title,:description,:link) RETURNING id",job)
            inserted = cursor.fetchone() != None

            if(inserted):
                self.connection.commit()
                return inserted
            else: 
                self.connection.rollback()
                return inserted
        except Exception as e:
            #print(traceback.format_exc())
            raise Exception("Couldn't write job to database (this shouldn't happen)") from e
        finally:
            self.connection.rollback()



    def read_jobs(self) -> List[Dict[str,Any]]:
        cursor = self.connection.execute("SELECT * FROM jobs WHERE applied = 0")
        return [dict(row) for row in cursor.fetchall()]

    def change_apply_to_true(self,filter: Dict[str,str]) -> None:
        try:
            self.connection.execute("UPDATE jobs SET applied = 1 WHERE job_id = :job_id AND provider = :provider",filter)
        except Exception as e:
            self.connection.rollback()
            raise Exception("An error Occurred while changing to applied") from e
        
        self.connection.commit()
        return None