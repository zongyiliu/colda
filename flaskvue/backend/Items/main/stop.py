import json

from flask import Flask, session, request, g, current_app
from flask.helpers import url_for
from flask.json import jsonify
from datetime import datetime

from Items import db
# import BluePrint
from Items.main import main
from Items.models import User, Message, Matched
from Items.main.errors import error_response, bad_request
from Items.main.auth import token_auth


@main.route('/stop_task/', methods=['POST'])
@token_auth.login_required
def stop_task():

    data = request.get_json()

    if not data:
        return bad_request('You must post JSON data.')
    if 'task_id' not in data or not data.get('task_id'):
        return bad_request('task_id is required.')

    task_id = data.get('task_id')

    most_recent_round = 0
    query = Message.query.filter(Message.task_id == task_id, Message.test_indicator == "train").order_by(Message.rounds.desc()).first()
    if query is not None:
        most_recent_round = query.rounds + 1

    get_all_sponsor_assistors = Matched.query.filter(Matched.task_id == task_id, Matched.test_indicator == "train").all()
    sponsor_id = None
    if not get_all_sponsor_assistors:
        sponsor_id = get_all_sponsor_assistors[0].sponsor_id
    
    if sponsor_id == g.current_user.id:
        Message.query.filter(Message.task_id == task_id, Message.test_indicator == "train", Message.rounds == most_recent_round).delete()
        db.session.commit()
        
        all_sponsor_assistors = set()
        for row in get_all_sponsor_assistors:
            all_sponsor_assistors.add(row.sponsor_id)
            all_sponsor_assistors.add(row.assistor_id_pair)

        for user_id in all_sponsor_assistors:
            user = User.query.get_or_404(user_id)
            user.add_notification('unread train stop', user.stop_train_task(task_id, most_recent_round))
            db.session.commit()
        
        response = jsonify({"sponsor delete successfully": "successfully", "check sponsor": "true"})
        return response

    else:
        Message.query.filter(Message.task_id == task_id, Message.test_indicator == "train", Message.rounds == most_recent_round, Message.sender_id == g.current_ser.id).delete()
        db.session.commit()
        
        Message.query.filter(Message.task_id == task_id, Message.test_indicator == "train", Message.rounds == most_recent_round, Message.assistor_id == g.current_ser.id).delete()
        db.session.commit()
        
        response = jsonify({"assistor delete successfully": "successfully", "check sponsor": "false", "most recent round": most_recent_round})
        return response

@main.route('/stop_test/', methods=['POST'])
@token_auth.login_required
def stop_test():

    data = request.get_json()

    if not data:
        return bad_request('You must post JSON data.')
    if 'test_id' not in data or not data.get('test_id'):
        return bad_request('test_id is required.')

    test_id = data.get('test_id')

    # most_recent_round = 0
    # query = Message.query.filter(Message.test_id == test_id, Message.test_indicator == "test").order_by(Message.rounds.desc()).first()
    # if query is not None:
    #     most_recent_round = query.rounds + 1

    get_all_sponsor_assistors = Matched.query.filter(Matched.test_id == test_id, Matched.test_indicator == "test").all()
    
    Message.query.filter(Message.test_id == test_id, Message.test_indicator == "test").delete()
    db.session.commit()
    
    all_sponsor_assistors = set()
    for row in get_all_sponsor_assistors:
        all_sponsor_assistors.add(row.sponsor_id)
        all_sponsor_assistors.add(row.assistor_id_pair)

    for user_id in all_sponsor_assistors:
        user = User.query.get_or_404(user_id)
        user.add_notification('unread test stop', user.stop_test_task(test_id, None))
        db.session.commit()
    
    response = jsonify({"sponsor delete successfully": "successfully", "check sponsor": "true"})
    return response

    # else:
    #     Message.query.filter(Message.test_id == test_id, Message.test_indicator == "test", Message.rounds == most_recent_round, Message.sender_id == g.current_ser.id).delete()
    #     db.session.commit()
        
    #     Message.query.filter(Message.test_id == test_id, Message.test_indicator == "test", Message.rounds == most_recent_round, Message.assistor_id == g.current_ser.id).delete()
    #     db.session.commit()
        
    #     response = jsonify({"assistor delete successfully": "successfully", "check sponsor": "false", "most recent round": most_recent_round})
        # return response


    
      
    
