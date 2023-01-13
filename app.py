from flask import Flask
from flask import render_template, request

from unidecode import unidecode
from flask_wtf import FlaskForm
from wtforms import SubmitField
from wtforms.validators import DataRequired, Length
from wtforms import TextAreaField

from flask_bootstrap import Bootstrap 

from flask_wtf.file import FileField
from flask import request, redirect
from werkzeug.utils import secure_filename
import os




app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)


class TextForm(FlaskForm):
    text = TextAreaField('Quel est votre text ?', validators=[DataRequired(), Length(min=20)])    
    submit = SubmitField('Submit')
    
@app.route('/test_text', methods=['GET', 'POST'])
def test_text():
    text = None
    occurrence = None
    form = TextForm()
    if form.validate_on_submit():
        text = form.text.data   # aqui recupero la variable ingresada por el utilizador
        
        text_to_analyze = unidecode(text.lower())
        occurrence = text_to_analyze.count("paris")
        occurrence += text_to_analyze.count("ville de lumiere") # esta variable occurrence es el resultado del procesamiento, 
                                                                # que luego se muestra en la aplicacion
    
    return render_template('paris_template.html', form=form, text=text, occurrence= occurrence)    


@app.route('/welcome')
def welcome( ):
   return render_template('welcome.html')

class NameForm(FlaskForm):
    name = TextAreaField('Quel est votre nom ?', validators=[Length(min=1)])
    submit = SubmitField("Submit")
    
@app.route('/user', methods=['GET', 'POST'])
def user():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        print(name)
        
        # Gérer les valeurs saisies
    return render_template("user.html", form=form, name=name)

# con este metodo en html al usar:
# {% import "bootstrap/wtf.html" as wtf %}
# y luego abajo en el content
# {{ wtf.quick_form(form) }}
# con esto el reconoce automaticamente el formulario



class TextForm_2(FlaskForm):
    text = TextAreaField('Quel est votre text ?', validators=[DataRequired(), Length(min=20)])    
    submit = SubmitField('Submit')
    
class FileForm(FlaskForm):
    file = FileField('File')
    submit = SubmitField("Submit")

@app.route('/paris_2', methods=['GET', 'POST'])
def paris_2():
    text = None
    occurrence = None
    form = TextForm_2()
    if form.validate_on_submit():
        text = form.text.data   # aqui recupero la variable ingresada por el utilizador
        
        text_to_analyze = unidecode(text.lower())
        occurrence = text_to_analyze.count("paris")
        occurrence += text_to_analyze.count("ville de lumiere") # esta variable occurrence es el resultado del procesamiento, 
                                                                # que luego se muestra en la aplicacion
    
    UPLOAD_FOLDER = 'C:/Users/cesar/Documents/Dos/20230110_Benjamin_flask/projet_paris'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'csv'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    form_2 = FileForm()
    if form_2.validate_on_submit():
        uploaded_file = form_2.file.data
        if uploaded_file.filename != '':
            #uploaded_file.save(uploaded_file.filename)
            if uploaded_file and allowed_file(uploaded_file.filename):
                filename = secure_filename(uploaded_file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                uploaded_file.save(file_path )
                
                with open(file_path, encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    occurrence = 0
                    for line in lines:
                        text_to_analyze = unidecode(line.lower())
                        occurrence += text_to_analyze.count("paris")
                        occurrence += text_to_analyze.count("ville de lumiere") 
                        # print(line)  
        

    return render_template('paris_template_bootstrap.html', form=form, form_2=form_2, text=text, occurrence= occurrence) 


# class TextForm_login(FlaskForm):
#     name = TextAreaField('Utilisator : ', validators=[DataRequired(), Length(min=1)])
#     password = TextAreaField('Password : ', validators=[DataRequired(), Length(min=10)])
#     submit = SubmitField('Submit')
    
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     name = None
#     password = None
#     form = TextForm_login()
#     if form.validate_on_submit():
#         name = form.name.data
#         password = form.password.data
#         print(name, password)
        
#         # Gérer les valeurs saisies
#     return render_template("user.html", form=form, name=name)