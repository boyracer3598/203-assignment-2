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

@app.route('/greet/<name>',methods=['GET', 'POST'])
def greet(name):
    return render_template('greet.html', user_name=name)


# game stuff
# for games
@app.route('/games', methods=['GET', 'POST'])
def games():
    return render_template('gameMenu.html')


#for clicker game
count = 0
@app.route('/clicker', methods=['POST'])
def increment():
    global count
    count += 1
    return render_template('clicker.html', count=count)

# fidget spinner fidget
@app.route('/spinner',methods=['GET', 'POST'])
def spinner():
    return render_template('spinner.html')

# for squish fidget
@app.route('/squish',methods=['GET', 'POST'])
def squish():
    return render_template('squish.html')

# for balloon pop fidget
@app.route('/balloon', methods=['GET', 'POST'])
def ballon():
    return render_template('balloon.html')

# page for logging your mood
@app.route('/mood', methods=['GET', 'POST'])
def mood():
    if request.method == 'POST':
        mood = request.form['mood']
        print(f"User's mood: {mood}")
    return render_template('mood.html')

#run the application
if __name__ == '__main__':
    app.run(debug=True)

