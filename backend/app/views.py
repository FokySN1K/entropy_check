from flask import (render_template, session, request, url_for,
                   redirect, send_from_directory, flash)

from app import app, ALLOWED_EXTENSIONS
from functools import wraps
import uuid
import os

import entropy
from entropy import convert_file
from entropy import create_graphs_entr_hist


def allowed_file(filename):

    basename, extension = os.path.splitext(filename)
    return (extension in ALLOWED_EXTENSIONS)

def auth(func):
    @wraps(func)
    def wrapper():
        if 'uid' in session:
            return func()
        else:
            session['uid'] = uuid.uuid4()
            return 'Пожалуйста, перезагрузите страницу'

    return wrapper

def save_file_from_new_user(file):

    PATH = app.config['UPLOAD_FOLDER']
    directories = os.listdir(PATH)

    directory_path = PATH + str(session['uid']) + '/'
    file_path = directory_path + str(session['uid'])

    if str(session['uid']) in directories:
        files = os.listdir(PATH + str(session['uid']))
        for file1 in files:
            os.remove(directory_path + file1)
    else:
        os.mkdir(directory_path)

    file.save(file_path + ".txt")

"""
    Создаёт график энтропии и гистограммы для 3 видов файлов:
    обычного, зашифрованного и прошедшего процедуру Павла
    
"""
def create_graphs():

    PATH = app.config['UPLOAD_FOLDER']
    directory_path =  PATH + str(session['uid']) + '/'
    file_path =directory_path + str(session['uid']) + ".txt"

    '''
        Производим предобработку данных
    '''
    convert_file.convert_file_to_bin(directory_path, file_path)
    encrypt_file_path = convert_file.encrypt_file_convert_to_bin(directory_path, file_path)
    convert_file.low_entropy_algorithm_convert_to_bin(directory_path, encrypt_file_path)


    '''
        Строим графики энтропии
    '''
    create_graphs_entr_hist.create_graphs(directory_path)


@app.route('/download/<filename>')
def download(filename):
    try:
        return send_from_directory(f'static/USERS_FILE/{session['uid']}', filename)
    except:
        return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@auth
def index():

    if request.method == 'POST':

        if 'file' not in request.files:
            flash('Не могу прочитать файл')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('Нет выбранного файла')
            return redirect(request.url)

        if file and allowed_file(file.filename):

            try:
                save_file_from_new_user(file)
                create_graphs()
                return redirect(url_for('get_files'))
            except Exception as e:
                print(e)
                flash('Произошла ошибка')
                return redirect(request.url)
        else:
            flash('Файл должен быть в формате .txt')
            return redirect(request.url)

    return render_template("about.html",
                           user_id=session['uid'])


@app.route('/get_files/')
@auth
def get_files():
    directory_path = '/static/USERS_FILE/' + str(session['uid']) + '/'
    NAMES_ENTR = [
                [directory_path + entropy.ENTROPY + entropy.BIN + entropy.PNG, "Энтропия файла"],
                [directory_path + entropy.ENTROPY + entropy.ENCRYPT + entropy.PNG, "Энтропия зашифрованного файла"],
                [directory_path + entropy.ENTROPY + entropy.ALGO + entropy.PNG, "Энтропия файла после алгоритма"],
                [directory_path + entropy.HISTOGRAM + entropy.BIN + entropy.PNG, "Гистограмма файла"],
                [directory_path + entropy.HISTOGRAM + entropy.ENCRYPT + entropy.PNG, "Гистограмма зашифрованного файла"],
                [directory_path + entropy.HISTOGRAM + entropy.ALGO + entropy.PNG, "Гистограмма файла после алгоритма"],
    ]

    PATH = app.config['UPLOAD_FOLDER']
    directories = os.listdir(PATH)

    directory_path = PATH + str(session['uid']) + '/'
    file_path = directory_path + str(session['uid'])

    if str(session['uid']) in directories:
        return render_template("entropy.html",
                               url = NAMES_ENTR, user_id = session['uid'])
    else:
        flash("Что-то пошло не так")
        return redirect("index")
