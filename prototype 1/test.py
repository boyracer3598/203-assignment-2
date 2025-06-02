from flask import Flask, request,render_template
# from PTL import Image
import io
app = Flask(__name__)   

count = 0


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/increment', methods=['POST'])
def increment():
    global count
    count += 1
    return render_template('index.html', count=count)

if __name__ == '__main__':
    app.run(debug=True)