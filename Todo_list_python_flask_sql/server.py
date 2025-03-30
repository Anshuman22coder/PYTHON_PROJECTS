from flask import Flask,render_template, request, redirect, url_for
import cx_Oracle

app=Flask(__name__)
tasks=[]

def get_db_connection():
  conn=cx_Oracle.connect("system/1123@localhost")
  return conn
@app.route('/')
def home():
    conn = get_db_connection()
    curr = conn.cursor()
    
    # Fetch all tasks from the database
    curr.execute("SELECT * FROM Task")
    f = curr.fetchall()
    
    # Clear the `tasks` list before repopulating it
    tasks.clear()
    
    # Populate `tasks` list from the database rows
    for row in f:
        tasks.append(row[1])  # Assuming the second column is the task name
    
    curr.close()
    conn.close()
    
    return render_template("index.html", tasks=tasks)



@app.route("/add",methods=["POST"])
def add():
  task=request.form.get("task")
  if task:
    tasks.append(task)
  l=len(tasks)-1 # last index where we have to store the new task in the db .
  if request.method=="POST":
    conn=get_db_connection()
    curr=conn.cursor()
    curr.execute("Insert into Task values(:1,:2)",(l,tasks[l]))
    conn.commit()
    curr.close()

  return redirect(url_for("home"))   # goes to the / route and as url_for()function takes the route function name as input that's why we use home not /.

@app.route("/delete/<int:task_id>")
def delete (task_id):
  if task_id>=0 and task_id<len(tasks):
    
    conn=get_db_connection()
    curr=conn.cursor()
    task_name=tasks[task_id]
    curr.execute("Delete from Task where taskname=:1",(task_name,))
    
    conn.commit()
    tasks.pop(task_id)
    curr.close()
    conn.close()
  
  return redirect(url_for("home"))

if __name__=="__main__":
  app.run(debug=True)