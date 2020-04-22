import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_EXTENSIONS = {'png','jpg','jpeg'}
    UPLOAD_FOLDER = os.path.join(os.getcwd(),"app/static/uploads/")
    APIKEY = "p_YLm5EGcKi-oS7IfTQrjtY0HstOq1ZY"