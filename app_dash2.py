from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileField 
from wtforms import TextAreaField
from wtforms import SubmitField
from wtforms.validators import DataRequired, Length
from flask_bootstrap import Bootstrap
#from flask import SQLAlchemy
import os

import pandas as pd
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

from db.config import Config
from db.extensions import db
from db.models.user import User

import plotly.express as px



app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjhfdkjhgjkdfhgkjdfhg'
bootstrap = Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

dash_app = Dash(
    __name__,
    server=app,
    url_base_pathname='/dash/',
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

LOGO = "https://gretaformation.ac-orleans-tours.fr/sites/all/themes/themes/adscom/images/logo.jpg"

navbar = dbc.Navbar(
    color="dark", dark=True,
    children=[dbc.Container([
        html.A(
            href="/dash", style={"textDecoration": "none"},
            children=dbc.Row(
                align="center", className="g-0",
                children=[
                    dbc.Col(html.Img(src=LOGO, height="36px")),
                    dbc.Col(dbc.NavbarBrand("Navbar", className="ms-2")),
                ]),

        )]),
        dbc.NavItem(dbc.NavLink("Home", href="/", external_link=True)),
    ])

data = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

dash_app.layout = html.Div(children=[
    navbar,
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for your data.
    '''),
])

fig = px.bar(data, x="Fruit", y="Amount", color="City", barmode="group")

dash_app.layout = html.Div(children=[navbar, dcc.Graph(id='example-graph', figure=fig)])

app.config.from_object(Config)
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route("/dash")
def my_dash_app():
    return dash_app.index()

class UserForm(FlaskForm):
    username = TextAreaField('Username : ', validators=[Length(min=1)])
    email = TextAreaField('Email : ', validators=[Length(min=1)])
    password = TextAreaField('Password : ', validators=[Length(min=1)])
    submit = SubmitField("Submit")

@app.route("/user", methods=['GET', 'POST'])
def user_creation():
    username = None
    email = None
    password = None
    
    form = UserForm()
    if form.validate_on_submit():
        # username = request.args["username"]
        # email = request.args["email"]
        # password = request.args["password"]
        
        username = form.username.data
        email = form.email.data
        password = form.password.data
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()       
        
    return render_template('user_db.html', form=form, username=username, email=email, password=password)


@app.route("/user/<username>", methods=['PUT'])
def user_update(username):
    email = request.args["email"]
    password = request.args["password"]
    db.session.query(User).filter(User.username == username).update(
        {"email": email, "password": password}, synchronize_session="fetch"
    )
    db.session.commit()
    return "ok"


@app.route("/user/<username>", methods=['DELETE'])
def user_delete(username):
    user = User.get_by_username(username)
    db.session.delete(user)
    db.session.commit()
    return "ok"


@app.route("/user/<username>", methods=['GET'])
def user_get(username):
    user = User.get_by_username(username)
    return str(user)


# @app.route("/users", methods=['GET'])
# def user_search():
#     query = request.args["query"]
#     users = db.session.query(User).filter(User.email.like(f'%{query}%')).all()
#     return users

@app.route("/users", methods=['GET'])
def users():
    users = db.session.query(User).all()
    print(users)
    return render_template("all_users_db.html", users=users)