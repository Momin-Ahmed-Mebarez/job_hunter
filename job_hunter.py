#TODO change to bulk inseration in the database
from pathlib import Path
from db_handle import DBHandle
import sqlite3,time
from flask import Flask,render_template,g,request
from winsound import Beep
from queue import Queue
from threading import Thread

#Modules to check for sites (each module handles a site)
from targets import sabbar



HOME = Path(__file__).resolve().parent

app = Flask(__name__)
db_queue = Queue()

def get_handle() -> DBHandle:
    if "db" not in g:
        g.connection = sqlite3.connect(HOME / "jobs.db",timeout=30)
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
    connection = sqlite3.connect(HOME / "jobs.db")
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
    while True:
        try:
            jobs = sabbar.update_jobs()
            for job in jobs:
                print(job)
                pass




                #db_queue.put({"operation":"new","data":job})
        except Exception as e:
            print(e)
        print("Updated jobs")
        time.sleep(60 * 30)


#END OF RUNNING THREADS

def init_db():
    connection = sqlite3.connect(HOME / "jobs.db")
    #Only one time
    #connection.execute("PRAGMA journal_mode=WAL;")
    #connection.execute("PRAGMA synchronous=NORMAL;")
    
    #DBHandle(connection).drop_tables()

   
    DBHandle(connection).init_db()
    connection.close()


#Routes 
@app.route("/")
def main():
    handle = get_handle()
    valid_jobs = handle.read_jobs()

    return render_template("index.html",valid_jobs=valid_jobs)

@app.route("/apply",methods=["POST"])
def apply():
    job_id = request.args.get("job_id")
    provider = request.args.get("provider")
    data = {"job_id":job_id,"provider":provider}
    db_queue.put({"operation":"update","data":data})
    return "200"

if __name__ == "__main__":
    init_db()
    
    db_thread = Thread(target=write_to_db,daemon=True)
    jobs_thread = Thread(target=check_for_jobs,daemon=True)
    
    db_thread.start()
    jobs_thread.start()

    app.run(debug=True,host="192.168.1.62",use_reloader=False)
