from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import psycopg2

app = Flask(__name__, template_folder='template')
app.secret_key = 'secretkeyofjp'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:neha2408@localhost/user'
db = SQLAlchemy(app)


class User(db.Model):
    id1 = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def Home():
    if request.method == 'POST':

        email = request.form.get('email')
        password = request.form.get('password')

        us = User.query.filter_by(email=email).first()

        if us.email == email:
            if us.password == password:
                flash('You are logged in')
                session['us.id'] = us.id1
                return redirect(url_for('List'))
            else:
                flash('Invalid Credentials')

    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def Signup():
    if request.method == 'POST':
        p1 = request.form.get('password')
        p2 = request.form.get('password2')
        if p1 == p2:
            user = User(request.form['name'], request.form['email'], request.form['password'])
            db.session.add(user)
            db.session.commit()
        else:
            flash('Password not match')

    return render_template('signup.html')


@app.route('/list')
def List():
    return render_template('list.html', users=User.query.all())


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def Delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return render_template('list.html', users=User.query.all())


if __name__ == "__main__":
    app.run(debug=True)


