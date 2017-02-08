#!/usr/bin/env python3

import requests
from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy 
#from sqlalchemy.dialects import postgresql
from datetime import datetime


app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

class ContactRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False)
    email = db.Column(db.String(120), unique=False)
    message = db.Column(db.String(500), unique=False)
    date = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, name, email, message):
        self.name = name
        self.email = email
        self.message = message

    def __repr__(self):
        return '{name} ({email}): {message}'.format(name=self.name,
                                                    email=self.email,
                                                    message=self.message,)


def validate_recaptcha(recap_token):
    payload = { 'secret': app.config['RECAP_SECRET'],
                'response': recap_token }

    r = requests.post(app.config['RECAP_URL'], data=payload)
    
    if r.status_code == 200:
        try:
            r_j = r.json()
        except:
            pass
        else:
            if r_j['success']:
               return True
    
    return False


@app.route('/blog/contact', methods=['POST'])
def contact():
    if validate_recaptcha(request.form['g-recaptcha-response']):
        new_request = ContactRequest(request.form['name'],
                                     request.form['email'],
                                     request.form['message'],)
        db.session.add(new_request)
        db.session.commit()

    return redirect('https://gazwald.com/')


if __name__ == '__main__':
    app.run(
        host = "0.0.0.0",
        port = 8000,
    )
