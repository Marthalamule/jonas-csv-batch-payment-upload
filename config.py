import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY =  os.environ.get('SECRET_KEY') or os.urandom(24)

    @staticmethod
    def init_app(app):
        pass


config = {
    'default':Config
}