from flask import Flask, render_template, request, session, redirect
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

db = client['Plagarism']

app = Flask(__name__)
app.secret_key = 'password'
users = db['users']


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/signin')
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = db.users.find_one(
            {'username': username, 'password': password})
        if user:
            session['username'] = user['username']
            return render_template('home.html')
        else:
            return render_template('signin.html', result="Invalid username or password")

    return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['email']
        password = request.form['password']

        if db.users.find_one({'username': username}):
            return render_template('signup.html', result="Username already exists")

        user_data = {'username': username, 'password': password,
                     'firstname': firstname, 'lastname': lastname}
        db.users.insert_one(user_data)

        session['username'] = username
        return redirect('/')

    return render_template('signup.html')


app.add_url_rule("/signup", 'signup', signup)
app.add_url_rule("/signin", 'signin', signin)

if __name__ == "__main__":
    app.run(debug=True)
