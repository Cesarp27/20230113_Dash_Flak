from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField 
from wtforms import SubmitField
from flask_bootstrap import Bootstrap
#from flask import SQLAlchemy
import os

from dash import Dash, dcc, html

app = Flask(__name__)
dash_app = Dash(
    __name__,
    server=app,
    url_base_pathname='/dash/'
)

dash_app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
])


@app.route("/dash")
def my_dash_app():
    return dash_app.index()