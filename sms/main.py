#!/usr/bin/python2.6
# -*-coding: utf-8 -*-
__author__ = 'egor.koba'

import datetime
import pyexcel_xls
from flask.ext import excel
from form import ReportForm
from werkzeug.contrib import cache
from webargs.flaskparser import use_args
from webargs import Arg, ValidationError
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.contrib.cache import SimpleCache
from flask import Flask, request, render_template

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
cache = SimpleCache()
send_args = {
    'subscriber'   : Arg(int, required=True, validate=lambda val: len(str(val)) == 11),
    'serviceNumber': Arg(str, required=True, validate=lambda val: len(val) > 0),
    'timestamp'    : Arg(str, required=True, validate=lambda val: validate_date(val)),
    'reporttime'   : Arg(str, required=True, validate=lambda val: validate_date(val)),
    'status'       : Arg(int, required=True, validate=lambda val: val >= 0 | val <= 1)
}

class Subscribers(db.Model):
    __tablename__ = 'subscribers'
    id            = db.Column(db.Integer, primary_key=True)
    subscriber    = db.Column(db.Integer)
    serviceNumber = db.Column(db.Integer)
    reporttime    = db.Column(db.DateTime)
    timestamp     = db.Column(db.DateTime)
    status        = db.Column(db.Boolean)

    def __init__(self, subscriber, serviceNumber, reporttime, timestamp, status):
        self.subscriber    = subscriber
        self.serviceNumber = serviceNumber
        self.reporttime    = reporttime
        self.timestamp     = timestamp
        self.status        = status

    def to_object(self):
        return {
            'id': self.id,
            'subscriber'   : self.subscriber,
            'serviceNumber': self.serviceNumber,
            'reporttime'   : self.reporttime.isoformat(),
            'timestamp'    : self.timestamp.isoformat(),
            'status'       : self.status
            }

def validate_date(val):
    try:
        datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        raise ValidationError('Invalid datetime format')

def actQuery(subscriber, serviceNumber, timestamp_start, timestamp_finish, status):
    sql = "SELECT * FROM subscribers"
    where = []
    if status != '2':
        where.append("status = '%s'" % status)
    if subscriber != '':
        where.append("subscriber = '%s'" % subscriber)
    if serviceNumber != '':
        where.append("serviceNumber = '%s'" % serviceNumber)
    if timestamp_start != '':
        where.append("timestamp >= '%s'" % timestamp_start)
    if timestamp_finish != '':
        where.append("timestamp < '%s'" % timestamp_finish)
    if where:
        sql = '{0} WHERE {1}'.format(sql, ' AND '.join(where))
    return sql

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/send', methods=['GET'])
@use_args(send_args)
def send(args):
    subscriber    = args['subscriber']
    serviceNumber = args['serviceNumber']
    reporttime    = args['reporttime']
    timestamp     = args['timestamp']
    status        = args['status']
    insert        = Subscribers(subscriber, serviceNumber, reporttime, timestamp, status)
    db.session.add(insert)
    db.session.commit()
    return 'Ok'

@app.route('/report', methods=['GET', 'POST'])
def report():
    form = ReportForm()
    return render_template('report.html', title='Report', form=form)


@app.route('/result', methods=['GET', 'POST'])
def result():
    subscriber       = request.form['subscriber']
    serviceNumber    = request.form['serviceNumber']
    timestamp_start  = request.form['timestamp_start']
    timestamp_finish = request.form['timestamp_finish']
    status           = request.form['status']
    query   = actQuery(subscriber, serviceNumber, timestamp_start, timestamp_finish, status)
    cur     = db.engine.execute(query)
    results = [dict(id=row[0],
            subscriber=row[1],
         serviceNumber=row[2],
            reporttime=row[3],
             timestamp=row[4],
                status=row[5]) for row in cur.fetchall()]
    cache.set('sql_data', results, timeout=5 * 60)
    return render_template('result.html', results=results)

@app.route('/download')
def download():
    sql_data = cache.get('sql_data')
    response = excel.make_response_from_records(sql_data, 'xls')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0')