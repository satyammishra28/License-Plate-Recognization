from flask import render_template,redirect,request,flash,session,url_for
from flask_login import logout_user,current_user, login_user, login_required
from app import app,db
from app.models import User,MyUpload,Prediction
from datetime import datetime
from app.detector import detect_item
from werkzeug.utils import secure_filename
import os
import json
import cv2

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
            try:
                del session['last_image'] 
                del session['prediction']
            except:pass
            return redirect(request.url)
        else:
            flash('wrong file selected, only PNG and JPG images allowed','danger')
            return redirect(request.url)
   
    return render_template('upload.html',title='view uploads')

def showtext(filepath):
    try:
        del session['last_image'] 
        del session['prediction'] 
    except : pass
    servepath = filepath[filepath.find('static')-1:]
    text = detect_item(filepath,app.config.get('APIKEY'))
    img = cv2.imread(filepath)
    datadict  = json.loads(text)
    if datadict.get('message').lower() =='success':
        if 'result' in datadict:
            p = datadict.get('result')[0].get('prediction')[0]
            img = cv2.rectangle(img,(p['xmin'],p['ymin']),(p['xmax'],p['ymax']),(255,0,0,),2)
            cv2.imwrite(filepath,img)
        else:
            print("error, no result")
    else:
        print("error,failed")
    scan =Prediction(img_id=session['imgid'],output=text)
    db.session.add(scan)
    db.session.commit()
    session['last_image'] = servepath
    session['prediction'] = text
    return render_template('result.html',filename = servepath, data = json.loads(text))

@app.route('/predict')
def predict():
    if 'last_image' in session and 'prediction' in session:
        return render_template('result.html',filename = session['last_image'], data = json.loads(session['prediction']))
    elif 'path' in session:
        filename=session['path']
        if os.path.exists(filename):
            return showtext(filename)
        else: 
            flash("please upload a new image to view prediction","danger")
            return redirect("/upload")
    else:
        flash("please upload a new image to view prediction","warning")
        return redirect("/upload")

@app.route("/history")
def history():
    upload_path = '/static/uploads/'
    data = Prediction.query.all()[::-1]
    tabbed_data = []
    for i,item in enumerate(data):
        datadict  = json.loads(item.output)
        if datadict.get('message').lower() =='success':
            if 'result' in datadict:
                try:
                    rowdict= {}
                    pred_dict = datadict.get('result')[0].get('prediction')
                    filename =  datadict.get('result')[0].get('input')
                    rowdict['file'] = upload_path+filename
                    rowdict['result'] = pred_dict[0]
                    rowdict['date'] = item.created_on
                    rowdict['imgid'] = item.img_id
                    rowdict['id'] = item.id
                    tabbed_data.append(rowdict)
                except Exception as e:
                    pass
    return render_template('history.html', data=tabbed_data)


@app.route('/delete', methods=['POST'])
def delete_image():
    if request.method =='POST':
        imgid = request.form.get('imgid')
        id = request.form.get('id')
        try:
            row = db.session.query(Prediction).filter_by(id = id).first()
            db.session.delete(row)
            db.session.commit()
        except Exception as e:
            pass
        try:
            row = db.session.query(MyUpload).filter_by(id = imgid).first()
            print(row)
            db.session.delete(row)
            db.session.commit()
        except Exception as e:
            print(e)
        try:os.remove("app"+row.img)
        except:pass
        flash("data removed from database","success")
        return redirect('/history')

