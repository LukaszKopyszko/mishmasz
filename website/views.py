from flask import Blueprint, render_template, request,flash,redirect, url_for, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user = current_user)

@views.route('/user-notes', methods=['GET','POST'])
def notes():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 5:
            flash('Notatka jest za krótka, musi mieć co najmniej 6 znaków.', category = 'error')
        else:
            new_note = Note(data=note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Notatka pomyślnie dodana!', category='success')

    return render_template("user_notes.html", user = current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            
    return jsonify({})

@views.route('/bmi-calc', methods=['GET','POST'])
def bmi_calc():
    bmi = 0
    if request.method == 'POST':
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        option = request.form.get('options')
        if option == 'men':
            bmi = calc_bmi_men(weight,height)
        else:
            bmi = calc_bmi_women(weight,height)
    return render_template("bmi_calc.html", bmi=float(bmi), user = current_user)                
def calc_bmi_men(weight,height):
    return round((weight/((height/100)**2)),2)
def calc_bmi_women(weight,height):
    return round((weight/((height/100)**2)-1),2)
    


@views.route('/morse', methods=['GET', 'POST'])
def morse():

    morse_text = ''

    code_dict = {' ':'|', 'a':'.-', 'ą':'.-.-','b':'-...','c':'-.-.','ć':'-.-..','d':'-..','e':'.','ę':'..-..','f':'..-.','g':'--.','h':'....','i':'..','j':'.---','k':'-.-','l':'.-..',
    'ł':'.-..-','m':'--','n':'-.','ń':'--.--'
    , 'o':'---','ó':'---.', 'p':'.--.','q':'--.-','r':'.-.','s':'...','ś':'...-...','t':'..-','u':'..-','v':'..-','w':'.--','x':'-..-','y':'-.--','z':'--..','ź':'--..-','ż':'--..-.'}

    if request.method == 'POST':
        global text
        text = str(request.form.get('text_normal'))
        for letter in text:
            morse_text += code_dict[letter.lower()]
         
    return render_template("mors.html", user=current_user, morse_text = morse_text, text=text)


    @views.route('/math', methods=['GET','POST'])
    def math():


        return render_template("math.html", user=current_user)