from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
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

count = 0
#for clicker game
@app.route('/clicker', methods=['POST'])
def increment():
    global count
    count += 1
    return render_template('clicker.html', count=count)

@app.route('/spinner',methods=['GET', 'POST'])
def spinner():
    return render_template('spinner.html')

@app.route('/squish',methods=['GET', 'POST'])
def squish():
    return render_template('squish.html')

@app.route('/balloon', methods=['GET', 'POST'])
def ballon():
    return render_template('balloon.html')

#route for avatar creation and saving into an array

@app.route('/avatar',methods=['GET', 'POST'])
def avatar(): 
    return render_template('avatar.html')

#save into array
character_data = []
def save_avatar():
    data = request.json
    character_data.append(data) #saving data to the global list
    print("Character Data:", character_data)
    return jsonify(status='success', saved=data, total=len(character_data))
    

#run the application
if __name__ == '__main__':
    app.run(debug=True)

