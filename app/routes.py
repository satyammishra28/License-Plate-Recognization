from flask import render_template,redirect,request,flash,session,url_for
from flask_login import logout_user,current_user, login_user, login_required
from app import app,db
from app.models import User,MyUpload,Prediction
from datetime import datetime
from app.detector import detect_item
from werkzeug.utils import secure_filename
import os
import json

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',title='home')


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/upload', methods=['GET','POST'])
def uploadImage():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            flash('No file uploaded','danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('no file selected','danger')
            return redirect(request.url)
        if file and allowed_files(file.filename):
            print(file.filename)
            filename = secure_filename(file.filename)
            path=os.path.join(app.config['UPLOAD_FOLDER'], filename )
            file.save(path)
            upload = MyUpload(img =f"/static/uploads/{filename}", imgtype = os.path.splitext(file.filename)[1])
            db.session.add(upload)
            db.session.flush()
            session['imgid'] = upload.id
            db.session.commit()
            flash('file uploaded and saved','success')
            session['uploaded_file'] = f"/static/uploads/{filename}"
            session['path']=path
            return redirect(request.url)
        else:
            flash('wrong file selected, only PNG and JPG images allowed','danger')
            return redirect(request.url)
   
    return render_template('upload.html',title='upload new Image')

def showtext(filepath):
    servepath = filepath[filepath.find('static')-1:]
    text = detect_item(filepath,app.config.get('APIKEY'))
    print(text,type(text))
    scan =Prediction(img_id=session['imgid'],output=text)
    db.session.add(scan)
    db.session.commit()
    return render_template('result.html', filename = servepath, data = json.loads(text))

@app.route('/predict')
def predict():
    filename=session['path']
    return showtext(filename)

    

