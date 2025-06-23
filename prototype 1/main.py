from flask import Flask, render_template, request, url_for, redirect, flash,session
from time import sleep
import sqlite3
import datetime

#create a Flask application
#user1info = {
 #   "name": "Yoshi",
   # "email": "richard@gillingham.co.nz",
  #  "password": "12345678"
#}

app = Flask(__name__)
app.secret_key = "yoshi"

moodLog = []
global CurrentUser
CurrentUser = None

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
        #if the info entered matchs a entry in the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM accounts WHERE name = ? AND email = ? AND password = ?", (name, email, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            message = "Welcome back, {}!".format(user['name'])
            
        else:
            message = "Invalid credentials. Please try again."
            flash(message)
            #sleep(2)
            return render_template("index.html", message=message)

        session['current_user'] = user['name']
        #redirect to another page
        return redirect(url_for('greet'))

    else:
        message = ""
    return render_template("index.html", message=message)

@app.route('/greet', methods=['GET', 'POST'])
def greet():
    user_name = session.get('current_user', None)
    print(f"Current User: {user_name}")
    return render_template('greet.html', CurrentUser=user_name)

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
        #add the user to the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO accounts (name, email, password) VALUES (?, ?, ?)', (name, email, password))
        conn.commit()
        conn.close()
        #redirect to another page
        return redirect(url_for('index', name=name))

        
        

    return render_template("login.html", message="")

# game stuff
# for games
@app.route('/games', methods=['GET', 'POST'])
def games():
    return render_template('gameMenu.html', user_name=CurrentUser)


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

#get date and formate it
def get_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")



# page for logging your mood
@app.route('/mood', methods=['GET', 'POST'])
def mood():
    if request.method == 'POST':
        mood = request.form['mood']
        print(f"User's mood: {mood}")
        moodComment = request.form['mood_comment']
        print(f"User's mood comment: {moodComment}")
        # does not allow empty comment
        if( mood == "" or moodComment == ""):
            return render_template('mood.html')
        else:
            moodLog.append({'date':get_date(),'mood': mood, 'comment': moodComment})
            print(f"Mood log: {moodLog}") 
            # temp name for now
            name= 'User'
            # also go back to a page
            return redirect(url_for('greet', name=name))
    # if the request is a GET request, just render the mood page      
    return render_template('mood.html')



#route for avatar creation and saving into an array

@app.route('/avatar', methods=['GET', 'POST'])
def avatar():
    if request.method == 'POST':
        
        # get the shirt color
        shirt_color = request.form.get('shirt_color')
        print("Shirt Color:", shirt_color)

        if shirt_color == 'red':
            shirt_color = 'shirt2.png'
        elif shirt_color == 'blue':
            shirt_color = 'shirt1.png'

        # get the pants type
        pants_type = request.form.get('pants_type')
        print("Pants Type:", pants_type)

        if pants_type == 'jeans':
            pants_type = 'pants1.png'
        elif pants_type == 'shorts':
            pants_type = 'pants2.png'

        # get the shoe type
        shoe_type = request.form.get('shoe_type')
        print("Shoe Type:", shoe_type)
        
        if shoe_type == 'red boots':
            shoe_type = 'shoe1.png'
        elif shoe_type == 'sneakers':
            shoe_type = 'shoe2.png'

        # get the hair type
        hair_type = request.form.get('hair_type')
        print("Hair Type:", hair_type)

        if hair_type == 'long':
            hair_type = 'hair1.png'
        elif hair_type == 'short':
            hair_type = 'hair2.png'

        #send the shirt color to the link
        return redirect(url_for('avatar', shirt_color=shirt_color, pants_type=pants_type, shoe_type=shoe_type, hair_type=hair_type))
    return render_template('avatar.html', shirt_color=request.args.get('shirt_color', 'default.png'), pants_type=request.args.get('pants_type', 'default.png'), shoe_type=request.args.get('shoe_type', 'shoe2.png'), hair_type=request.args.get('hair_type', 'default.png'))

# page for mental health exercises
@app.route('/exercise', methods=['GET', 'POST'])
def exercise():
    return render_template('exercise.html')

@app.route('/exercise/meditation', methods=['GET', 'POST'])
def meditation():
    return render_template('meditation.html')

@app.route('/exercise/breathing', methods=['GET', 'POST'])
def breathing():
    return render_template('breathing.html')

@app.route('/exercise/grounding', methods=['GET', 'POST'])
def grounding():
    return render_template('grounding.html')

@app.route('/exercise/journaling', methods=['GET', 'POST'] )
def journaling():
    return render_template('journaling.html')

#run the application
if __name__ == '__main__':
    app.run(debug=True)