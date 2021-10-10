from flask import Flask, request, render_template,url_for,redirect
import sqlite3

app=Flask(__name__)
conn=sqlite3.connect('docpres.db')
cur=conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS docdetails (name TEXT,hospital TEXT, proficiency TEXT, email TEXT)")
conn.commit()
conn.close()



def insertValDoc(name, hospital, proficiency, email):
  conn=sqlite3.connect('docpres.db')
  cur=conn.cursor()
  cur.execute("INSERT INTO docdetails VALUES (?,?,?,?)",(name,hospital,proficiency,email))
  conn.commit()
  printTableDoc()
  conn.close()

def printTableDoc():
  conn=sqlite3.connect('docpres.db')
  cur=conn.cursor()
  cur.execute("SELECT * FROM docdetails")
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
  return render_template('dashboard.html',email=email,name=name,proficiency=proficiency,hospital=hospital)



@app.route('/newpres/<email>')
def newpres(email):
    return render_template('newpres.html',email=email)

@app.route('/makepres/<email>',methods=['POST'])
def makepres(email):
  pname=request.form['pname']
  print(pname)
  return redirect(url_for('dashboard',email=email,page=1))

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port='5000')
