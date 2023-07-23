from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
    "apiKey": "AIzaSyAW__Cg4XUxp2NUzXlYVDon5VHi6YWLw4o",
  "authDomain": "romie-projecty2.firebaseapp.com",
  "projectId": "romie-projecty2",
  "storageBucket": "romie-projecty2.appspot.com",
  "messagingSenderId": "117475133009",
  "appId": "1:117475133009:web:bc8074246472867b559a70",
  "measurementId": "G-2WMGZBQ69G",
  "databaseURL": ""

  }


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
   error = ""
   if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
   return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template("signup.html")
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)