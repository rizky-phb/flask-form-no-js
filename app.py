from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data

        # Check if username exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash("Username already exists", "error")
            return redirect(url_for('register'))

        # Check if email exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists", "error")
            return redirect(url_for('register'))

        # If neither username nor email exists, create a new user
        new_user = User(username=username, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash("User created successfully", "success")
        return redirect(url_for('register'))

    return render_template('register.html', form=form)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
