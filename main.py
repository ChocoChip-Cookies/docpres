from flask import Flask, request, render_template,url_for,redirect
import sqlite3
import random
from datetime import datetime
app=Flask(__name__)
conn=sqlite3.connect('docpres.db')
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS docdetails (name TEXT,hospital TEXT, proficiency TEXT, email TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS presdetails (pid TEXT,pname TEXT, docname TEXT, medlist TEXT,age INTEGER,Symptoms TEXT, Diagnosis TEXT, test TEXT, date_time_pres TEXT)")
conn.commit()
conn.close()

PIDlst=[]
def generatePID():
  global PIDlst
  pid=""
  for i in range(6):
    pid+=str(random.randint(0,10))
  if pid in PIDlst:
    generatePID()
  else:
    return pid

def insertValDoc(name, hospital, proficiency, email):
  conn=sqlite3.connect('docpres.db')
  cur=conn.cursor()
  cur.execute("INSERT INTO docdetails VALUES (?,?,?,?)",(name,hospital,proficiency,email))
  conn.commit()
  printTableDoc()
  conn.close()
def insertValPres(pid, pname,docname,medlist, age, symptoms, diagnosis, test, date_time_pres):
  conn=sqlite3.connect('docpres.db')
  cur=conn.cursor()
  cur.execute("INSERT INTO presdetails VALUES (?,?,?,?,?,?,?,?,?)",(pid,pname,docname,medlist,age,symptoms,diagnosis,test,date_time_pres))
  conn.commit()
  printTableDoc()
  conn.close()
def printTableDoc():
  conn=sqlite3.connect('docpres.db')
  cur=conn.cursor()
  cur.execute("SELECT * FROM presdetails")
  rows=cur.fetchall()
  print(rows)
  conn.close()
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/makeDoctor',methods=['POST'])

def makeDoctor():
  conn=sqlite3.connect('docpres.db')
  cur=conn.cursor()
  name=request.form['name']
  hospital=request.form['hospital']
  proficiency=request.form['proficiency']
  email=request.form['email']
  email = email.split("@")[0]+email.split("@")[1].split('.')[0]
  insertValDoc(name,hospital,proficiency,email)
  
  cur.execute("SELECT * FROM docdetails WHERE email=?",(email,))
  rows=cur.fetchall()
  print("PRINTING ROWS",rows)
  return redirect(url_for('dashboard',email=email,page=1))

@app.route('/dashboard/<page>/<email>')
def dashboard(page,email):
  conn=sqlite3.connect('docpres.db')
  cur=conn.cursor()
  
  if page=="1" or page=="3":
    #signup
    print(email)
    cur.execute("SELECT * FROM docdetails WHERE email=?",(email,))
    rows=cur.fetchall()
    print("PRINTING ROWS",rows)
  elif page=="2":
    email=email.split("@")[0]+email.split("@")[1].split('.')[0]
    cur.execute("SELECT * FROM docdetails WHERE email=?",(email,))
    rows=cur.fetchall()
    if rows==[]:
      return "No Such User"
    print("PRINTING ROWS - LOGIN:", rows)
  name=rows[0][0]
  proficiency=rows[0][2]
  hospital=rows[0][1]
  cur.execute("SELECT * FROM presdetails WHERE docname=?",(name,))
  lst = cur.fetchall()

  return render_template('dashboard.html',email=email,name=name,proficiency=proficiency,hospital=hospital, preshist = lst)



@app.route('/newpres/<email>')
def newpres(email):
    return render_template('newpres.html',email=email)

@app.route('/makepres/<email>',methods=['POST'])
def makepres(email):
  pname=request.form['pname']
  
  dob=request.form['dob']
  symptoms=request.form['symptoms']
  diagnosis=request.form['diagnosis']
  test=request.form['test']
  n=request.form['numofmed']
  meds=[]
  pid=generatePID()
  for i in range( 1,int(n)+1):
    med=[]
    med.append(request.form['med'+str(i)+'name'])
    med.append(request.form['med'+str(i)+'type'])
    med.append(request.form['med'+str(i)+'dosage'])
    med.append(request.form['med'+str(i)+'timing'])
    med.append(request.form['med'+str(i)+'frequency'])
    med.append(request.form['med'+str(i)+'duration'])
    meds.append(med)
  meds=str(meds)
  now = datetime.today().year
  dob= datetime.strptime(dob,"%Y-%m-%d").year
  age = (now-dob)
  conn=sqlite3.connect('docpres.db')
  cur=conn.cursor()
  cur.execute("SELECT * FROM docdetails WHERE email=?",(email,))
  docname=cur.fetchall()[0][0]
  conn.close()
  date_time_pres=str(datetime.now().strftime("%Y-%m-%d"))
  print(date_time_pres)
  insertValPres(pid, pname, docname,meds, age, symptoms,diagnosis,test,date_time_pres)
  printTableDoc()
  return redirect(url_for('printable',email=email,pid=pid))
@app.route('/printable/<email>/<pid>')
def printable(email,pid):
  conn=sqlite3.connect('docpres.db')
  cur=conn.cursor()
  cur.execute("SELECT * FROM docdetails WHERE email=?",(email,))
  docname =cur.fetchall()[0][0]
  cur.execute("SELECT * FROM docdetails WHERE email=?",(email,))
  hospital=cur.fetchall()[0][1]
  cur.execute("SELECT * FROM presdetails WHERE pid=?",(pid,))
  pname = cur.fetchall()[0][1]
  cur.execute("SELECT * FROM presdetails WHERE pid=?",(pid,))
  medlist = cur.fetchall()[0][3] 
  medlist=eval(medlist)
  cur.execute("SELECT * FROM presdetails WHERE pid=?",(pid,)) 
  age = cur.fetchall()[0][4]
  cur.execute("SELECT * FROM presdetails WHERE pid=?",(pid,))
  symptoms = cur.fetchall()[0][5]
  cur.execute("SELECT * FROM presdetails WHERE pid=?",(pid,))
  diagnosis = cur.fetchall()[0][6]
  cur.execute("SELECT * FROM presdetails WHERE pid=?",(pid,))
  test = cur.fetchall()[0][7]
  cur.execute("SELECT * FROM presdetails WHERE pid=?",(pid,))
  date_time_pres = cur.fetchall()[0][8]
  conn.close()
  return(render_template('printable.html',hospital=hospital,date = date_time_pres,pid = pid, name=pname, age= age,symptoms = symptoms,diagnosis=diagnosis,medlist = medlist, test = test))

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port='5000')
