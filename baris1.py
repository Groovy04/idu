from bokeh.models.ranges import FactorRange
from flask import Flask, render_template, flash, request, url_for, redirect
from flask_wtf import FlaskForm
from sqlalchemy.orm import session
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms import validators
from wtforms.validators import DataRequired, Email, ValidationError, InputRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

from flask_login import UserMixin
from flask_login import login_user, current_user, logout_user, login_required

from flask_login import LoginManager
from flask_bcrypt import Bcrypt

#from A_bokeh1 import script, div  #Arrange these in the file


#////////bokeh test libraries
import random
from bokeh.models.tools import Toolbar
import pandas
import numpy as np
import pandas as pd
import pandas

from bokeh.layouts import layout
from bokeh.models.glyphs import Circle
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure, output_file, save
from bokeh.io import curdoc, show
from numpy import source

from bokeh.sampledata.iris import flowers
from bokeh.models import Range1d, PanTool, ResetTool, HoverTool, Band, Toggle, Div
from bokeh.models.annotations import Label, LabelSet, Span, BoxAnnotation, ToolbarPanel
from bokeh.models.widgets import Select, Slider, RadioButtonGroup
from bokeh.layouts import gridplot, row, column
from bokeh.io import curdoc
from bokeh.transform import dodge
from bokeh.resources import CDN
from math import pi

from bokeh.embed import server_document, components

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine

from forms import Login, SalesMTPlanned, SalesMTActual, Customer1, Customer1_Search_Form


app = Flask(__name__)

bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://tansubaktiran:Avz9p9&9Dgsu_099@193.111.73.99/tansubaktiran"

#Secret key
app.config['SECRET_KEY'] = "$2b$12$P5vdQLFZE.7.Cji.aqKBZOJm8nOL4VT5hP0OWuhHQ216NL5nqAvie"
#Initialize the adatabase
db = SQLAlchemy(app)

#Setting up user login parts
"""login_manager = LoginManager(app)
login_manager.login_view = 'login' #Name of the route in charge of logging in
login_manager.login_message_category = 'info'"""


#ADDED FOR TESTING USER LOGIN - 27.10.21
"""@login_manager.user_loader
def load_user(id):
    return Users_db.query.get(int(id)) #DB table name to be updated!!!! ////////////"""


#DATABASE MODELS TO BE UPDATED - 
#AUTHORIZED USERS, SALESMTPLANNED, SALESMTACTUAL, CUSTOMERS, ... OTHERS?
class IDU_db(db.Model, UserMixin): #TO BE UPDATED!!!
    id = db.Column(db.Integer, primary_key=True)
    soru1_db = db.Column(db.String(200), nullable=False)
    soru2_db = db.Column(db.String(120), nullable=False)
    soru3_db = db.Column(db.String(120), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Name %r>' % self.id



class Anket(FlaskForm):
    soru1 = SelectField(label='1. Soru', choices=[("Hiç rahatsız etmez", "Hiç rahatsız etmez"), ("Pek rahatsız etmez", "Pek rahatsız etmez"), ("Fark etmez", "Fark etmez"), ("Biraz rahatsız eder", "Biraz rahatsız eder"),("Çok rahatsız eder", "Çok rahatsız eder")])
    soru2 = SelectField(label='2. Soru', choices=[("Hiç rahatsız etmez", "Hiç rahatsız etmez"), ("Pek rahatsız etmez", "Pek rahatsız etmez"), ("Fark etmez", "Fark etmez"), ("Biraz rahatsız eder", "Biraz rahatsız eder"),("Çok rahatsız eder", "Çok rahatsız eder")])
    soru3 = SelectField(label='3. Soru', choices=[("Hiç rahatsız etmez", "Hiç rahatsız etmez"), ("Pek rahatsız etmez", "Pek rahatsız etmez"), ("Fark etmez", "Fark etmez"), ("Biraz rahatsız eder", "Biraz rahatsız eder"),("Çok rahatsız eder", "Çok rahatsız eder")])
    submit = SubmitField("Save This Entry")
    



#////////endof - CUSTOMERS DB

#ROUTES
@app.route('/')
@app.route('/index', methods=["GET", "POST"])
def index():
    name="TEST"
    number = 10
    form=Anket()
    #global new_survey 
    if form.validate_on_submit():
        new_survey = IDU_db(
            soru1_db = form.soru1.data, 
            soru2_db = form.soru2.data,
            soru3_db = form.soru3.data, 
            )

        db.session.add(new_survey)
        db.session.commit()
    #flash("Entry recorded successfully! Thank you!", "success")
    
    return  render_template("index.html", name=name, number=number, form=form)
    

#//////////////////////////////
#//////////////////////////////BOKEH TEST REGION
#Dashboard Grafik kısmını ekleyeceğiz.
@app.route('/graph')

def graph():
    
    # Connecting to MySQL server using mysql-python DBAPI 
    engine = create_engine("mysql+pymysql://tansubaktiran:Avz9p9&9Dgsu_099@193.111.73.99/tansubaktiran")
    dbconnection = engine.connect()

    anket_data = pandas.read_sql("select * from IDU_db", dbconnection)
    #actual_data = pandas.read_sql("select * from SALESMTACTUAL_db", dbconnection)
    #myfilter = planned_data["year_planned_db"]==2022
    #planned_data.sort_values(by='id', ascending=True, inplace=True)
    #filtered_planned_data = planned_data[myfilter]
    soru1 = anket_data["soru1_db"]
    soru2 = anket_data["soru2_db"]
    soru3 = anket_data["soru3_db"]

    ozet1=soru1.value_counts()
    print(ozet1.index)
    ozet2=soru2.value_counts()
    #source1 = ColumnDataSource(soru1)
    ozet3=soru3.value_counts()

    f1 = figure(x_range=list(ozet1.index))
    f1.circle(x=list(ozet1.index), y=ozet1, size=20, fill_alpha=.5, color="limegreen", legend_label="Soru 1")
    
    f2 = figure(x_range=list(ozet2.index))
    f2.circle(x=list(ozet2.index), y=ozet2, size=20, fill_alpha=.5, color="orangered", legend_label="Soru 2")

    f3 = figure(x_range=list(ozet3.index))
    f3.circle(x=list(ozet3.index), y=ozet3, size=20, fill_alpha=.5, color="turquoise", legend_label="Soru 3")
    
    #print(anket_data["soru1_db"])
    #print(anket_data["soru1_db"].describe())
    #df['column_name']. value_counts(normalize=True)
    summary_of_categorical = anket_data.value_counts(normalize=True)
    #print(summary_of_categorical.index, type(summary_of_categorical))
    source = ColumnDataSource(anket_data)
    #print(source.data)

    """f = figure(x_range=list(summary_of_categorical.index))
    f.circle(x=dodge('index', -0.15, range=f.x_range), y="soru1_db", size=20, fill_alpha=.5, 
    color="limegreen", source=source1, legend_label="Test")"""

    #f1 = figure(x_range=list(sum_USD_2019.index), title="Storbridge - 2019 and 2020 USD Currency EXc Rates - Basic Statistics")
    
    """f1 = figure(x_range=list(source1.data["index"]), title="Storbridge - 2019 and 2020 USD Currency Exch. Rates") #Her ikisi de oluyor.
    f1.y_range = Range1d(start=0, end=8)
    f1.square(x=dodge('index', -0.15, range=f1.x_range), y="USD Satış Kuru", size=20, fill_alpha=.5, 
    color="limegreen", source=source1, legend_label="2019")
    f1.square(x=dodge('index', 0.15, range=f1.x_range), y="USD Satış Kuru", size=20, fill_alpha=.5, 
    color="orangered", source=source2, legend_label="2020")"""
    
    f1.y_range = Range1d(start=0, end=10)
    f1.xaxis.major_label_orientation = pi/6
    f2.y_range = Range1d(start=0, end=10)
    f2.xaxis.major_label_orientation = pi/6
    f3.y_range = Range1d(start=0, end=10)
    f3.xaxis.major_label_orientation = pi/6
    #show(f)

    lay_out = gridplot([[f1,f2, f3]],plot_width=400, plot_height=500)
    #show(lay_out)
    script, div = components(lay_out)

    return  render_template("graph.html", script=script, div=div)



if __name__ == "__main__":
    app.run(debug=True)