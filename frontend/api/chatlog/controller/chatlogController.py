#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import io
from frontend import settings
from Helper.mongo_connection import MongoConnection
from flask import make_response
from datetime import datetime, timedelta


def get_chatlogs_with_limit(value):
    """
                This service can be used for list chat logs with limit. Mongo query gets last recorded logs according
                to defined limit
    """
    connection = MongoConnection(db=settings.MONGODB_DB, host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    collection = connection.get_collection('chatlogs')
    return list(collection.find().sort([('creation_date', -1)]).limit(value))


def get_csv_export_for_all_chatlogs():
    """
                    This service can be used for export chat logs. Csv include below values;
                    - input
                    - username
                    - current_threshold
                    - intent
                    - confidence
                    - creation_date
                    - preConfidence
                    - preIntent

    """
    df = pd.DataFrame(
        columns=['input', 'username', 'current_threshold', 'intent', 'confidence', 'creation_date', 'preConfidence',
                 'preIntent'])
    connection = MongoConnection(db=settings.MONGODB_DB, host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    collection = connection.get_collection('chatlogs')
    for x in collection.find():
        df = df.append({'input': x['input'],
                        'username': x['context']['username'],
                        'current_threshold': x['current_threshold'],
                        'intent': x['intent']['id'],
                        'confidence': x['intent']['confidence'],
                        'creation_date': x['creation_date'],
                        'preConfidence': x['preConfidence'],
                        'preIntent': x['preIntent'],
                        }, ignore_index=True)
    out = io.StringIO()
    df.to_csv(out)
    resp = make_response(out.getvalue())
    resp.headers["Content-Disposition"] = "attachment; filename=all_chatlogs.csv"
    resp.headers["Content-type"] = "text/csv; charset=utf-8"
    resp.headers["Content-Encoding"] = "utf-8"
    return resp


def get_csv_export_for_all_intents():
    """
                    This service can be used for export all intents. Csv include below values;
                    - id
                    - text
                    - speechResponse

    """
    connection = MongoConnection(db=settings.MONGODB_DB, host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    collection = connection.get_collection('intent')
    df = pd.DataFrame(list(collection.find()))
    df['speechResponse'].replace(regex=True, inplace=True, to_replace=r'\n', value=r'')
    out = io.StringIO()
    df.to_csv(out)
    resp = make_response(out.getvalue())
    resp.headers["Content-Disposition"] = "attachment; filename=all_intents.csv"
    resp.headers["Content-type"] = "text/csv; charset=utf-8"
    resp.headers["Content-Encoding"] = "utf-8"
    return resp


def get_csv_export_for_chatlogs_acoording_to_date(year, month, day):
    """
                        This service can be used for export chat logs from posted date to now. Csv include below values;
                        - input
                        - username
                        - current_threshold
                        - intent
                        - confidence
                        - creation_date
                        - preConfidence
                        - preIntent

    """
    df = pd.DataFrame(
        columns=['input', 'username', 'current_threshold', 'intent', 'confidence', 'creation_date', 'preConfidence',
                 'preIntent'])
    connection = MongoConnection(db=settings.MONGODB_DB, host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    collection = connection.get_collection('chatlogs')
    start = datetime(year, month, day)
    end = datetime.now()

    for x in collection.find({"creation_date": {'$lte': end, '$gte': start}}):
        df = df.append({'input': x['input'],
                        'username': x['context']['username'],
                        'current_threshold': x['current_threshold'],
                        'intent': x['intent']['id'],
                        'confidence': x['intent']['confidence'],
                        'creation_date': x['creation_date'],
                        'preConfidence': x['preConfidence'],
                        'preIntent': x['preIntent'],
                        }, ignore_index=True)
    out = io.StringIO()
    df.to_csv(out)
    resp = make_response(out.getvalue())
    resp.headers["Content-Disposition"] = "attachment; filename=all_chatlogs.csv"
    resp.headers["Content-type"] = "text/csv; charset=utf-8"
    resp.headers["Content-Encoding"] = "utf-8"
    return resp


def get_csv_export_for_chatlogs_acoording_to_lastdate(value):
    """
                        This service can be used for export chat logs from posted date to now. Csv include below values;
                        - input
                        - username
                        - current_threshold
                        - intent
                        - confidence
                        - creation_date
                        - preConfidence
                        - preIntent

    """
    now = datetime.utcnow()
    last_d = now - timedelta(days=value)
    df = pd.DataFrame(
        columns=['input', 'username', 'current_threshold', 'intent', 'confidence', 'creation_date', 'preConfidence',
                 'preIntent'])
    connection = MongoConnection(db=settings.MONGODB_DB, host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    collection = connection.get_collection('chatlogs')

    for x in collection.find({"creation_date": {"$gte": last_d}}):
        df = df.append({'input': x['input'],
                        'username': x['context']['username'],
                        'current_threshold': x['current_threshold'],
                        'intent': x['intent']['id'],
                        'confidence': x['intent']['confidence'],
                        'creation_date': x['creation_date'],
                        'preConfidence': x['preConfidence'],
                        'preIntent': x['preIntent'],
                        }, ignore_index=True)
    out = io.StringIO()
    df.to_csv(out)
    resp = make_response(out.getvalue())
    resp.headers["Content-Disposition"] = "attachment; filename=all_chatlogs.csv"
    resp.headers["Content-type"] = "text/csv; charset=utf-8"
    resp.headers["Content-Encoding"] = "utf-8"
    return resp


def get_chatlogs_session_count():
    """
                This service can be used for count os chat sessions
    """
    connection = MongoConnection(db=settings.MONGODB_DB, host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    collection = connection.get_collection('chatlogs')
    result = {}
    result['result'] = collection.count()
    return result


def get_chatlogs_fallback_count():
    """
                This service can be used for count of fallbacks
    """
    connection = MongoConnection(db=settings.MONGODB_DB, host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    collection = connection.get_collection('chatlogs')
    result = {'result': collection.find({'intent.id': 'fallback'}).count()}
    return result


def get_chatlogs_sessions_count_last_x_days(value):
    """
                This service can be used for count of fallbacks in 30 days
    """
    now = datetime.utcnow()
    last_d = now - timedelta(days=value)
    connection = MongoConnection(db=settings.MONGODB_DB, host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    collection = connection.get_collection('chatlogs')
    result = {'result': collection.find({"creation_date": {"$gte": last_d}}).count()}
    return result


def get_chatlogs_fallbacks_count_last_x_days(value):
    """
                This service can be used for count of fallbacks in 30 days
    """
    now = datetime.utcnow()
    last_d = now - timedelta(days=value)
    connection = MongoConnection(db=settings.MONGODB_DB, host=settings.MONGODB_HOST, port=settings.MONGODB_PORT)
    collection = connection.get_collection('chatlogs')
    result = {'result': collection.find({'intent.id': 'fallback', "creation_date": {"$gte": last_d}}).count()}
    return result
