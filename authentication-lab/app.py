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
  "databaseURL": "https://romie-projecty2-default-rtdb.europe-west1.firebasedatabase.app/"

  }


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

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
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       full_name = request.form['full_name']
       username = request.form['username']
       bio = request.form['bio']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {
            'email': email,
            'full_name': full_name, 
            'username': username, 
            'bio': bio
            }
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
    return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
        UID = login_session['user']['localId']
        title = request.form['title']
        text = request.form['text']
        try:
            tweet = {
            'title': title,
            'text': text,
            'uid': UID
            }
            db.child("Users").child("Tweets").push(tweet)
        except:
            print("Couldn't add Tweet")

    return render_template("add_tweet.html")

@app.route('/all_tweets')
def tweets():
    tweets = db.child("Users").child("Tweets").get().val()
    return render_template("tweets.html", tweets = tweets)




if __name__ == '__main__':
    app.run(debug=True)