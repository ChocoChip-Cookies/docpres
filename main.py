from flask import Flask, request, render_template,url_for


app=Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')
#@app.route('/makeDoctor')

@app.route('/dashboard/<name>')
def dashboard(name):
    return render_template('dashboard.html',name=name)


if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0',port='5000')
