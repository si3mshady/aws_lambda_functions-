from flask import Flask, render_template, url_for

app=application=Flask(__name__)


@app.route('/')
def index():
     return render_template('index.html')


@app.route('/add')
def add():
     return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True, port=888, host='0.0.0.0')