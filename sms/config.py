#!/usr/bin/python
#-*-coding: utf-8 -*-
__author__ = 'egor.koba'

MYSQL_DB     = 'sms'
MYSQL_USER   = 'flask'
MYSQL_PORT   = '3306'
MYSQL_TABLE  = 'subscribers'
MYSQL_HOST   = 'localhost'
MYSQL_PASSWD = 's3cur3pa55w0rd'

DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = 'hahaha'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASSWD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)