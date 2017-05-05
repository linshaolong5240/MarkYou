# -*- coding: utf-8 -*-

class Config:
    SECRET_KEY = 'underthemask'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:594120@localhost/underthemask?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    POSTS_PER_PAGE = 3

class DevelopmentConfig(Config):
    DEBUG = True

config = {
        'default':DevelopmentConfig,
        }
