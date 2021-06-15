import uuid
import json

from sqlalchemy import update
from flask import Flask, session, request, g, current_app
from flask.helpers import url_for
from flask.json import jsonify
from datetime import datetime

from Items import db

# import BluePrint
from Items.main import main

from Items.models import User, matched, Matched
from Items.main.errors import error_response, bad_request
from Items.main.auth import token_auth


@main.route('/match_sponsor_id/', methods=['POST'])
@token_auth.login_required
def match_sponsor_id():

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    if 'File' not in data or not data.get('File'):
        return bad_request('File is required.')
    if 'task_id' not in data or not data.get('task_id'):
        return bad_request('task_id is required.')

    data_array = json.loads(data['file'])
    task_id = data.get('task_id')

    # hardcode 
    # user = User.query.get_or_404(5)
    # if g.current_user == user:
    #     return bad_request('You cannot send private matched to yourself.')
    # response = Matched.query.filter(Matched.sponsor_id == g.current_user, task_id = task_id).with_entities(Matched.Matched_id_file)

    # response is a list
    response = Matched.query.filter(Matched.sponsor_id == g.current_user, Matched.task_id == task_id)

    # count the distinct id in the Sponsor ID file
    data_array_id = {}
    for i in range(1,len(data_array)):
        if data_array[i][0] not in data_array_id:
            data_array_id[data_array[i][0]] = 1

    for row in response:

        # already store a match id file
        if row.Matched_id_file:

            same_id = {}
            db_array = json.loads(row.Matched_id_file)
            
            # previous stored id
            for i in range(len(db_array)):
                if db_array[i] in data_array_id:
                    same_id[db_array[i]] = 1

            # Store the key, dont need the value
            same_id_keys = []
            for i in same_id.keys():
                same_id_keys.append(i)
            
            # update the db
            Matched.query.filter(Matched.task_id == task_id, Matched.recipient_id_pair == row.recipient_id_pair).update({"Matched_id_file": jsonify(same_id_keys)})

        else:

            # first time store the ID file, extract the first column (dont need to store the whole file)
            data_array_id = []
            for i in range(1,len(data_array)):
                data_array_id.append(data_array[i][0])

            # update the db
            Matched.query.filter(Matched.task_id == task_id, Matched.recipient_id_pair == row.recipient_id_pair).update({"Matched_id_file": jsonify(data_array_id)})
        
    db.session.commit()

    # send matched notification to the recipient
    user = User.query.get_or_404(g.current_user.id)
    user.add_notification('unread match id', user.new_match_id()) 
                        
    dict = {"stored": "stored"}
    response = jsonify(dict)

    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('main.get_matched', id=matched.id)
    
    return response

@main.route('/match_recipient_id/', methods=['POST'])
@token_auth.login_required
def match_recipient_id():

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    if 'File' not in data or not data.get('File'):
        return bad_request('File is required.')
    if 'task_id' not in data or not data.get('task_id'):
        return bad_request('task_id is required.')

    task_id = data.get('task_id')

    # Update last_requests_read_time
    user = User.query.get_or_404(g.current_user.id)
    last_requests_read_time = user.last_messages_read_time or datetime(1900, 1, 1)
    # one record for a recipient_id_pair per task
    record = Matched.query.filter(Matched.recipient_id_pair == g.current_user, Matched.task_id == task_id)

    # If can be omitted
    if last_requests_read_time > record['request_timestamp']:
        user.last_requests_read_time = record['request_timestamp']

        # submit to database
        db.session.commit()
        
        # Updata Notification
        user.add_notification('unread request', user.new_request()) 


    data_array = json.loads(data['file'])

    # hardcode 
    # user = User.query.get_or_404(5)
    # if g.current_user == user:
    #     return bad_request('You cannot send private matched to yourself.')
    # response = Matched.query.filter(Matched.sponsor_id == g.current_user, task_id = task_id).with_entities(Matched.Matched_id_file)

    # response is a list
    response = Matched.query.filter(Matched.sponsor_id == g.current_user, Matched.task_id == task_id)

    # count the distinct id in the Sponsor ID file
    data_array_id = {}
    for i in range(1,len(data_array)):
        if data_array[i][0] not in data_array_id:
            data_array_id[data_array[i][0]] = 1

    for row in response:

        # already store a match id file
        if row.Matched_id_file:

            same_id = {}
            db_array = json.loads(row.Matched_id_file)
            
            # previous stored id
            for i in range(len(db_array)):
                if db_array[i] in data_array_id:
                    same_id[db_array[i]] = 1

            # Store the key, dont need the value
            same_id_keys = []
            for i in same_id.keys():
                same_id_keys.append(i)
            
            # update the db
            Matched.query.filter(Matched.task_id == task_id, Matched.recipient_id_pair == row.recipient_id_pair).update({"Matched_id_file": jsonify(same_id_keys)})

        else:

            # first time store the ID file, extract the first column (dont need to store the whole file)
            data_array_id = []
            for i in range(1,len(data_array)):
                data_array_id.append(data_array[i][0])

            # update the db
            Matched.query.filter(Matched.task_id == task_id, Matched.recipient_id_pair == row.recipient_id_pair).update({"Matched_id_file": jsonify(data_array_id)})
        
    db.session.commit()

    # send matched notification to the recipient
    user = User.query.get_or_404(g.current_user.id)
    
    user.add_notification('unread match id', user.new_match_id()) 
                        
    dict = {"stored": "stored"}
    response = jsonify(dict)

    response.status_code = 201
    # HTTP协议要求201响应包含一个值为新资源URL的Location头部
    response.headers['Location'] = url_for('main.get_matched', id=matched.id)
    
    return response