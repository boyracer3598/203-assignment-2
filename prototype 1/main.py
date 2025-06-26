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
        # add one to the logins column in the database for the current user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET logins = logins + 1 WHERE name = ?", (user['name'],))
        conn.commit()
        conn.close()
        print(f"User {user['name']} logged in successfully.")
        #redirect to another page
        return redirect(url_for('greet'))

    else:
        message = ""
    return render_template("index.html", message=message)

def get_average_mood():
    #select all the moods for the mood_logs table from the current user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT mood FROM mood_logs WHERE account_id = (SELECT id FROM accounts WHERE name = ?)", (session.get('current_user', None),))
    moods = cursor.fetchall()
    conn.close()
    if not moods:
        return "No mood data available."
    mood_values = {'happy': 4, 'excited' : 5, 'neutral': 3, 'sad': 2, 'angry': 1}
    total_score = 0
    for mood in moods:
        total_score += mood_values.get(mood['mood'], 0)
    average_score = total_score / len(moods)
    return average_score
    

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


@app.route("/trackmood", methods=["GET", "POST"])
def track_mood():
    #check if there are any mood logs in the database for the current user, if not then set the average mood to 0
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM mood_logs WHERE account_id = (SELECT id FROM accounts WHERE name = ?)", (session.get('current_user', None),))
    count = cursor.fetchone()[0]
    conn.close()
    if count == 0:
        print("No mood logs found for the current user.")
        return render_template("trackmood.html", average_mood=0, moveleft=0, mood_logs=[], mile1=False, mile2=False, mile3=False, mile4=False)
    current_mood_average = get_average_mood()
    average_score = current_mood_average
    print(f"Average Mood Score: {average_score}")
    if average_score > 4:
        mood_translations = "excited"
    elif average_score > 3:
        mood_translations = "happy"  
    elif average_score > 2:
        mood_translations = "neutral"
    elif average_score > 1:
        mood_translations = "sad"
    else:
        mood_translations = "angry"
    # calculate how far the user needs to move left based on the average score
    moveleft = 150 * (5 - average_score)

    # send the mood logs to the trackmood.html page
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mood_logs WHERE account_id = (SELECT id FROM accounts WHERE name = ?)", (session.get('current_user', None),))
    mood_logs = cursor.fetchall()
    conn.close()
    print(f"Mood Logs: {mood_logs}")

    #get total amount of mood logs
    total_mood_logs = len(mood_logs)
    if total_mood_logs > 0:
        #add 10 points to the database points column of the current user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET points = points + 10 WHERE name = ?", (session.get('current_user', None),))
        #set mile1 in the database to 1 if it is 0
        cursor.execute("UPDATE accounts SET mile1 = 1 WHERE name = ? AND mile1 = 0", (session.get('current_user', None),))

        conn.commit()
        conn.close()
        print(f"Points added to user {session.get('current_user', None)}")
    print(f"Total Mood Logs: {total_mood_logs}")
    # if there are no mood logs, set the mood logs to an empty list
    if not mood_logs:
        mood_logs = []
    # if the user is not logged in, redirect to the login page
    if not session.get('current_user'):
        flash("You must be logged in to track your mood.")
        return redirect(url_for('login'))
    
    # check if mile1 is 1, if it is then set milestone1 to True
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT mile1 FROM accounts WHERE name = ?", (session.get('current_user', None),))
    mile1 = cursor.fetchone()
    conn.close()
    if mile1 and mile1['mile1'] == 1:
        milestone1 = True
    else:
        milestone1 = False

    # check if mile2 is 1, if it is then set milestone2 to True
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT mile2 FROM accounts WHERE name = ?", (session.get('current_user', None),))
    mile2 = cursor.fetchone()
    conn.close()
    if mile2 and mile2['mile2'] == 1:
        milestone2 = True
    else:
        milestone2 = False

    # check if mile3 is 1, if it is then set milestone3 to True
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT mile3 FROM accounts WHERE name = ?", (session.get('current_user', None),))
    mile3 = cursor.fetchone()
    conn.close()
    if mile3 and mile3['mile3'] == 1:
        milestone3 = True
    else:
        milestone3 = False

    #check if the user has excercised, if they have then set milestone4 to True
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT excerised FROM accounts WHERE name = ?", (session.get('current_user', None),))
    excerised = cursor.fetchone()
    conn.close()
    if excerised and excerised['excerised'] == 1:
        milestone4 = True
        #set mile4 to 1 in the database if it is 0 for the current user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET mile4 = 1 WHERE name = ? AND mile4 = 0", (session.get('current_user', None),))
        conn.commit()
        conn.close()
        print("Mile4 set to 1 for user:", session.get('current_user', None))
    else:
        milestone4 = False

    # check if mile4 is 1, if it is then set milestone4 to True
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT mile4 FROM accounts WHERE name = ?", (session.get('current_user', None),))
    mile4 = cursor.fetchone()
    conn.close()
    if mile4 and mile4['mile4'] == 1:
        milestone4 = True
    else:
        milestone4 = False

    #check if the user has logged in at least 3 times, if they have then set milestone 3 to True
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT logins FROM accounts WHERE name = ?", (session.get('current_user', None),))
    logins = cursor.fetchone()
    conn.close()
    if logins and logins['logins'] >= 3:
        milestone3 = True
    else:
        milestone3 = False
    

    # send the current mood average to the trackmood.html page
    return render_template("trackmood.html", average_mood=current_mood_average, moveleft=moveleft, mood_logs=mood_logs, mile1=milestone1, mile2=milestone2, mile3=milestone3, mile4=milestone4)

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
            # add the mood to the database with the id number of the user
            # get the current user from the session
            current_user = session.get('current_user', None)
            if not current_user:
                flash("You must be logged in to log your mood.")
                return redirect(url_for('login'))
            conn = get_db_connection()
            cursor = conn.cursor()
            #get the id of the current user
            cursor.execute("SELECT id FROM accounts WHERE name = ?", (current_user,))
            user = cursor.fetchone()
            if not user:
                flash("User not found.")
                return redirect(url_for('login'))
            current_user_id = user['id']
            #get the current user email
            cursor.execute("SELECT email FROM accounts WHERE name = ?", (current_user,))
            user_email = cursor.fetchone()
            if not user_email:
                flash("User email not found.")
                return redirect(url_for('login'))
            current_user_email = user_email['email']
            # insert the mood log into the database
            print(f"Inserting mood log for user {current_user} with email {current_user_email}")
            # create a new row in the mood_logs table
            # mood_logs table has account_id, name, email, mood, timestamp, comment

            cursor.execute('INSERT INTO mood_logs (account_id, name, email, mood, comment) VALUES (?, ?, ?, ?, ?)', (current_user_id, current_user, current_user_email, mood, moodComment))
            # commit the changes to the database
            conn.commit()


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

        # set mile2 to 1 in the database if it is 0 for the current user
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE accounts SET mile2 = 1 WHERE name = ? AND mile2 = 0", (session.get('current_user', None),))
        conn.commit()
        conn.close()
        print("Mile2 set to 1 for user:", session.get('current_user', None))
        
        

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
    return render_template('avatar.html', shirt_color=request.args.get('shirt_color', 'shirt1.png'), pants_type=request.args.get('pants_type', 'pants1.png'), shoe_type=request.args.get('shoe_type', 'shoe2.png'), hair_type=request.args.get('hair_type', 'hair2.png'))

# page for mental health exercises
@app.route('/exercise', methods=['GET', 'POST'])
def exercise():
    # set excercised to 1 in the database if it is 0 for the current user
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE accounts SET excerised = 1 WHERE name = ? AND excerised = 0", (session.get('current_user', None),))
    conn.commit()
    conn.close()
    print("Exercised set to 1 for user:", session.get('current_user', None))

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


#logout route
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    # clear the session
    session.clear()
    flash("You have been logged out.")
    print("User logged out.")
    # redirect to the index page
    return redirect(url_for('index'))

#run the application
if __name__ == '__main__':
    app.run(debug=True)