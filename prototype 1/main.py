from flask import Flask, render_template, request, url_for, redirect, flash
from time import sleep
import sqlite3

#create a Flask application
user1info = {
    "name": "Yoshi",
    "email": "richard@gillingham.co.nz",
    "password": "12345678"
}

app = Flask(__name__)
app.secret_key = "yoshi"

def get_db_connection():
    conn = sqlite3.connect('accounts.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form['name']
        while True:
            email = request.form['email']
            if '@' in email and '.' in email:
                break
            else:
                message = "Invalid email format. Please try again."
                flash(message)
                #sleep(2)
                return render_template("index.html", message=message)
        
        password = request.form['password']
        if len(password) < 8:
            message = "Password must be at least 8 characters long."
            flash(message)
            #sleep(2)
            return render_template("index.html", message=message)
        # Process the data (e.g., save to a database, print to console)
        print(f"Name: {name}, password: {password}, email: {email}")
        #if the info entered mtchs the user1info dictionary
        if name == user1info['name'] and email == user1info['email'] and password == user1info['password']:
            message = "Welcome back, Yoshi!"
        else:
            message = "Invalid credentials. Please try again."
            flash(message)
            #sleep(2)
            return render_template("index.html", message=message)

        #redirect to another page
        return redirect(url_for('greet', name=name))
    
    else:
        message = ""
    return render_template("index.html", message=message)

@app.route('/greet/<name>')
def greet(name):
    return render_template('greet.html', user_name=name)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form['name']
        while True:
            email = request.form['email']
            if '@' in email and '.' in email:
                break
            else:
                message = "Invalid email format. Please try again."
                flash(message)
                #sleep(2)
                return render_template("login.html", message=message)
        
        password = request.form['password']
        if len(password) < 8:
            message = "Password must be at least 8 characters long."
            flash(message)
            #sleep(2)
            return render_template("login.html", message=message)
        # Process the data and save to database accounts.db
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE name = ? AND email = ? AND password = ?", (name, email, password))
        user = cursor.fetchone()
        conn.close()

        
        

    return render_template("login.html", message="")


#run the application
if __name__ == '__main__':
    app.run(debug=True)