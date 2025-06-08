from flask import Flask, render_template, request, url_for, redirect, flash
from time import sleep

#create a Flask application
app = Flask(__name__)
app.secret_key = "yoshi"

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
        #redirect to another page
        return redirect(url_for('greet', name=name))
    
    else:
        message = ""
    return render_template("index.html", message=message)

@app.route('/greet/<name>')
def greet(name):
    return render_template('greet.html', user_name=name)

#run the application
if __name__ == '__main__':
    app.run(debug=True)