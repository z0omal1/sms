#!/usr/bin/python2.6
# -*-coding: utf-8 -*-
__author__ = 'egor.koba'

import datetime
from flask.ext.wtf import Form
from wtforms import DateTimeField, IntegerField, SelectField, validators

now = datetime.datetime.now()

class ReportForm(Form):
    subscriber       = IntegerField('tel', [validators.Length(min=11, max=11)], default=None)
    serviceNumber    = IntegerField('phoneshort', default=None)
    timestamp_start  = DateTimeField('starttime', format='%Y-%m-%d %H:%M:%S', default=datetime.datetime(2000, 01, 01, 0, 0, 0))
    timestamp_finish = DateTimeField('endtime', format='%Y-%m-%d %H:%M:%S', default=now)
    status           = SelectField('status',
    choices=[(0, u'недоставленные'),
             (1, u'доставленные'),
             (2, u'все')], default=2)
