from flask import Flask
from flask import request
from flask import render_template
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    user_agent = request.headers.get('user-agent')
    return render_template('index.html',user_agent=user_agent)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',user_name=name)

if __name__ == "__main__":
    app.run(debug = True)
