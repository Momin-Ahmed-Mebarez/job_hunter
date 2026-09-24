#TODO change to bulk inseration in the database
from pathlib import Path
import sqlite3,time,json
from threading import Thread
from queue import Queue
from winsound import Beep

from flask import Flask,render_template,g,request,redirect,url_for

from helpers.db_handle import DBHandle
from helpers.api_keeper import store_keys

#Modules to check for sites (each module handles a site)
from targets import sabbar



HOME = Path(__file__).resolve().parent
config = {}

app = Flask(__name__)
db_queue = Queue()

def get_handle() -> DBHandle:
    if "db" not in g:
        g.connection = sqlite3.connect(HOME / "helpers" / "jobs.db",timeout=30)
        g.connection.row_factory = sqlite3.Row
        g.db = DBHandle(g.connection)
    return g.db

@app.teardown_appcontext
def close_connection(error=None):
    connection = g.pop("connection", None)
    db = g.pop("db", None)

    if(connection):
        connection.close()

#Running therads
def write_to_db():
    connection = sqlite3.connect(HOME / "helpers" / "jobs.db")
    handle = DBHandle(connection)
    
    while True:
        task = db_queue.get()
        try:
            if(task["operation"] == "update"):
                handle.change_apply_to_true(task["data"])
            if(task["operation"] == "new"):
                handle.add_job(task["data"])
        except Exception as e:
            print(e)
        finally:
            db_queue.task_done()

def check_for_jobs():
    #TODO Move these lines into a function
    connection = sqlite3.connect(HOME / "helpers" / "jobs.db")
    handle = DBHandle(connection)
    
    while True:
        updated = False
        jobs = []
        try:
            jobs.extend(sabbar.update_jobs())
            for job in jobs:
                is_duplicate = handle.check_job_exists({"job_id":job["job_id"],"provider":job["provider"]})

                if(is_duplicate):
                    continue
                
                updated = True
                db_queue.put({"operation":"new","data":job})
        except Exception as e:
            print(e)

        if(updated):
            print("Updated jobs list")
            Beep(650,850)        
        
        updated = False
        time.sleep(60 * 30)


#END OF RUNNING THREADS

#Initialize functions
def init_db():
    connection = sqlite3.connect(HOME / "helpers" / "jobs.db")
    #Only one time
    #connection.execute("PRAGMA journal_mode=WAL;")
    #connection.execute("PRAGMA synchronous=NORMAL;")
    
    #DBHandle(connection).drop_tables()

   
    DBHandle(connection).init_db()
    connection.close()

def load_config():
    global config 
    with open(HOME / "config.json") as f:
        try:
            config = json.loads(f.read())
        except Exception as e:
            config = {}


#Routes 
@app.route("/")
def main():
    if(not config):
        return redirect(url_for("config"))

    handle = get_handle()
    valid_jobs = handle.read_jobs()
    
    return render_template("index.html",valid_jobs=valid_jobs)

@app.route("/config",methods=["POST","GET"])
def config():
    if(request.method == "POST"):
            validate_job_desc = bool(request.form.get("validate"))
            
            cv_llm_link = request.form.get("cv_llm_link")
            cv_llm_model = request.form.get("cv_llm_model")
            cv_llm_key = request.form.get("cv_llm_api_key")

            title_llm_link = request.form.get("title_llm_link")
            title_llm_model = request.form.get("title_llm_model")
            title_llm_key = request.form.get("title_llm_api_key")

            job_llm_link = request.form.get("job_llm_link")
            job_llm_model = request.form.get("job_llm_model")
            job_llm_key = request.form.get("job_llm_api_key")


            config_dict = {"validate_job_desc":validate_job_desc,
                           "cv_llm_link":cv_llm_link,
                           "cv_llm_model":cv_llm_model,
                           "title_llm_link": title_llm_link,
                           "title_llm_model": title_llm_model,
                           "job_llm_link":job_llm_link,
                           "job_llm_model":job_llm_model,
                           "job_sites":{"sabbar":True}}
            
            with open(HOME / "config.json", "w") as f:
                json.dump(config_dict,f,indent=4)
            
            store_keys(cv_llm_key,title_llm_key,job_llm_key)
            
            load_config()
            return redirect(url_for("main"))
    return render_template("config.html")

@app.route("/test",methods=["POST","GET"])
def test():
    if(request.method == "POST"):
            return redirect(url_for("main"))
    return render_template("cv.html")


#Route called by checkbox to change job state to applied
@app.route("/apply",methods=["POST"])
def apply():
    job_id = request.args.get("job_id")
    provider = request.args.get("provider")
    
    data = {"job_id":job_id,"provider":provider}
    db_queue.put({"operation":"update","data":data})
    
    return "200"


if __name__ == "__main__":
    init_db()
    load_config()

    db_thread = Thread(target=write_to_db,daemon=True)
    jobs_thread = Thread(target=check_for_jobs,daemon=True)
    
    db_thread.start()
    jobs_thread.start()

    app.run(debug=True,host="192.168.1.64",use_reloader=False)
