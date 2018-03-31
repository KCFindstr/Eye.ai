import os
from flask import Flask, request, redirect, url_for, flash, send_file, render_template, send_from_directory
from werkzeug.utils import secure_filename
import requests
import json
from config import *

app = Flask(__name__)

# allowed format
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'pdf'])
# UPLOAD_FOLDER set in the config.py
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "UPLOAD"
# introduction http://flask.pocoo.org/docs/0.12/quickstart/#static-files
# url_for('static', filename='style.css')

# used to store pictures's name
photoGallary = []
UPPER_SIZE_photoGallary = 20;

# testing html
html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>picture upload</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=file>
         <input type=submit value=upload>
    </form>
'''


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/home', methods=['PUT', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)  # use secure_filename function for safety
            # update the file & clean the photo cache
            cleanPhotoCache()
            print(photoGallary)
            print(request.form)
            # revise the filename with order
            filename = filename.rsplit('.', 1)[0].lower() + str(len(photoGallary)) + "." + \
                       filename.rsplit('.', 1)[1].lower()
            photoGallary.append(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(request.url)


@app.route('/', methods=['GET', 'POST'])
def home():
    '''
    #first render the template, then send post
    return redirect(url_for('upload_file'))
    '''
    cleanPhotoCache()
    if request.method == 'POST':
        print(request.form)
        #  upload the photo
        upload_file()
        if (request.form['tracking'] == "true"):
            print("get tracking request")
            # TODO return json package
            return situationAnalysis()
        else:
            # it is the request for detecting
            print("get detecting request")
        print(url_for('upload_file'))
    return render_template('Launch.html')


def situationAnalysis():
    # array of dictionary
    situation = [
        {"name": "Lion", "xPos": 100, "yPos": 100.5, "area": 2500, "motion": "to the right", "dangerLevel": 0.7},
        {"name": "Tiger", "xPos": 200, "yPos": 10.5, "area": 250, "motion": "to the right", "dangerLevel": 0.8},
        {"name": "UFO", "xPos": 50, "yPos": 140.5, "area": 700, "motion": "to the right", "dangerLevel": 0.9}
    ]
    in_json = json.dumps(situation)  # Encode the data
    return in_json


def cleanPhotoCache():
    # get all files in the upload folder
    photoGallary = os.listdir(app.config['UPLOAD_FOLDER'])
    # if there are files not belong to the folder, ignore them
    for files in photoGallary:
        if not allowed_file(files):
            photoGallary.remove(files)
    # delete files if more than limit
    while len(photoGallary) > UPPER_SIZE_photoGallary:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], photoGallary[0]))
        del photoGallary[0]


if __name__ == "__main__":
    app.run()

'''
# original method, used for storage
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename) #use secure_filename function for safety
            # update the file & clean the photo cache
            photoGallary.append(filename)
            cleanPhotoCache()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return redirect(request.url)
    return html

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)

# download from the Internet
@app.route('/uploads/test_download_Net/<filename>')
def download_file(url_addr):
    url = url_addr  # user provides url in query string
    r = requests.get(url, allow_redirects=True)

    # write to a file in the app's instance folder
    # come up with a better file name
    with app.open_instance_resource('downloaded_file', 'wb') as f:
        f.write(r.content)


@app.route('/uploads/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    if request.method == "GET":
        if os.path.isfile(os.path.join('upload', filename)):
            return send_from_directory('upload', filename, as_attachment=True)
            # return send_from_directory('upload', filename, as_attachment=True)#original line
'''
