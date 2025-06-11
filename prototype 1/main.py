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

#run the application
if __name__ == '__main__':
    app.run(debug=True)

