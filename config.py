# -*- coding: utf-8 -*-

class Config:
    SECRET_KEY = 'MarkYou'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:594120@localhost/mysql_markyou?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(Config):
    DEBUG = True

config = {
        'default':DevelopmentConfig,
        }
