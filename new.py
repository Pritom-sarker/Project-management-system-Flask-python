#   importing necesary file from flask
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from forms import searchFile

import os
from werkzeug.utils import secure_filename
import pandas as pd


app = Flask(__name__)
db = SQLAlchemy(app)

#   generate a secret key for forms
app.config['SECRET_KEY'] = '94692de71c05d2759ecc4bfd5d5ec4f0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['TEXT_FILE_UPLOAD'] = './static/text_files'
app.config['ALLOWED_IMAGE_EXTENSION'] = 'TXT'



class work(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    Date = db.Column(db.String())
    Work = db.Column(db.String())
    Last_Update = db.Column(db.String())
    Owner = db.Column(db.String())
    Budget = db.Column(db.String())
    Team = db.Column(db.String())
    Cost = db.Column(db.String())
    Total_Earning = db.Column(db.String())
    Des = db.Column(db.String())
    Status = db.Column(db.String())

    def __repr__(self):
        return f"work('{self.Date}','{self.Work}','{self.Date}','{self.Last_Update}','{self.Owner}','" \
               f"{self.Budget}','{self.Team}','{self.Cost}','{self.Total_Earning}','{self.BDT}','{self.Status}','" \
               f"{self.action})"


class people(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String())
    user = db.Column(db.String())
    password = db.Column(db.String())

    def __repr__(self):
        return f"people('{self.position}','{self.user}','{self.password})"

# df = pd.read_csv('POS.csv')
#
# for ind,data in df.iterrows():
#
#         row= work(Date=data[0],
#         Work=data[1],
#         Last_Update =data[2],
#         Owner=data[3],
#         Budget=data[4],
#         Team=data[5],
#         Cost=data[6],
#         Total_Earning=data[7],
#         Des='',
#         Status=data[9],)
#
#         db.session.add(row)
# db.session.commit()
row= people(position='Team',
user='CCC',
password ='12345')

db.session.add(row)
db.session.commit()
