from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import forms

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = '123'

db = SQLAlchemy(app)

@app.get('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LogInForm()
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignUpForm()
    return render_template('signup.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
