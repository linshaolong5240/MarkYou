# -*- coding: utf-8 -*-
import os

class Config:
    SECRET_KEY = 'underthemask'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:12345678@localhost/UTM?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # UPLOAD_FOLDER = '/Users/mark/uploads/'
    # UPLOAD_FOLDER = 'D:\\Users\\Mark\\uploads\\'
    UPLOAD_FOLDER = os.path.join(os.environ['HOME'],'upload')
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    POSTS_PER_PAGE = 5

class DevelopmentConfig(Config):
    DEBUG = True

config = {
        'default':DevelopmentConfig,
        }
