import json

from flask import Flask, session, request, g, current_app
from flask.helpers import url_for
from flask.json import jsonify
from datetime import datetime
from Items.main.utils import log, generate_msg

from Items import db
# import BluePrint
from Items.main import main
# from Items.models import User, Message, Matched, Stop
from Items.main.errors import error_response, bad_request
from Items.main.auth import token_auth
from Items.main.utils import obtain_user_id_from_token, obtain_unique_id
from Items.main.utils import verify_token_user_id_and_function_caller_id
from Items.main.mongoDB import mongoDB
from Items.main.mongoDB import train_match, train_message
from Items.main.mongoDB import test_match, test_message

@main.route('/stop_train_task/<string:id>', methods=['POST'])
@token_auth.login_required
def stop_train_task(id):

    """
    user terminates specific train task.
    If the user is sponsor, the whole train task will be terminated.
    If the user is assistor, it will not receive any message from this train task.

    Parameters:
       task_id - String. The id of train task
       
    Returns:
        If sponsor:
            response = {
                "message": "delete successfully", 
                "isSponsor": True, 
                "cur_rounds_num": cur_rounds_num
            }
        elif assistor:
            response = {
                "message": "delete successfully", 
                "isSponsor": False, 
                "cur_rounds_num": cur_rounds_num
            }

    Raises:
        KeyError - raises an exception
    """

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    if 'task_id' not in data or not data.get('task_id'):
        return bad_request('task_id is required.')

    task_id = data.get('task_id')

    user_id = obtain_user_id_from_token()
    user_document = mongoDB.search_user_document(user_id=id,username=None, email=None, key_indicator='user_id')
    # check if the caller of the function and the id is the same
    if not verify_token_user_id_and_function_caller_id(user_id, user_document['user_id']):
        return error_response(403)

    # check if the current client is the sponsor
    isSponsor = False
    train_match_document = train_match.search_train_match_document(task_id=task_id)
    sponsor_id = train_match_document['sponsor_information']['sponsor_id']
    assistor_information = train_match_document['assistor_information']
    sponsor_information = train_match_document['sponsor_information']
    sponsor_random_id = sponsor_information[sponsor_id]['sponsor_id_to_random_id']
    asssistor_random_id_mapping = train_match_document['asssistor_random_id_mapping']
    if sponsor_id == user_id:
        isSponsor = True 

    # get recent round
    cur_rounds_num = None
    train_message_document = train_message.search_train_message_document(task_id=task_id)
    # if train_message_document is None, it means it is the first round of this train_task
    if train_message_document is None:
        cur_rounds_num = 1
    else:
        cur_rounds_num = train_message_document['cur_rounds_num']

    if isSponsor:
        # delete the stopped round in train_message Table
        # train_mongoDB.delete_rounds_in_train_message_output_document(task_id=task_id, cur_rounds_num=cur_rounds_num, role='sponsor')
        
        # put sponsor in sponsor_terminate_id_dict
        train_match.update_user_stop_in_train_match_document(task_id=task_id, user_id=user_id, role='sponsor')

        # add stop notification to all sponsor and assistors' notification table
        for assistor_id in assistor_information:
            mongoDB.update_notification_document(user_id=assistor_id, notification_name='stop_train_task', 
                                                       id=task_id, sender_random_id=sponsor_random_id, 
                                                       role='assistor', cur_rounds_num=cur_rounds_num, test_indicator='train')

        mongoDB.update_notification_document(user_id=sponsor_id, notification_name='stop_train_task', 
                                                       id=task_id, sender_random_id=sponsor_random_id, 
                                                       role='sponsor', cur_rounds_num=cur_rounds_num, test_indicator='train')
   
        response = {
            "message": "delete successfully", 
            "isSponsor": True, 
            "cur_rounds_num": cur_rounds_num
        }
    elif not isSponsor:
        # delete the stopped round in train_message Table
        # train_mongoDB.delete_rounds_in_train_message_output_document(task_id=task_id, cur_rounds_num=cur_rounds_num)
        
        # put sponsor in sponsor_terminate_id_dict
        train_match.update_user_stop_in_train_match_document(task_id=task_id, user_id=user_id, role='assistor')
        assistor_id = user_id
        assistor_random_id = asssistor_random_id_mapping[assistor_id]

        # add stop notification to its notification table
        mongoDB.update_notification_document(user_id=assistor_id, notification_name='stop_train_task', 
                                                   id=task_id, sender_random_id=assistor_random_id, 
                                                   role='assistor', cur_rounds_num=cur_rounds_num, test_indicator='train')
   
        response = {
            "message": "delete successfully", 
            "isSponsor": False, 
            "cur_rounds_num": cur_rounds_num
        }
    return jsonify(response)



@main.route('/stop_test_task/<string:id>', methods=['POST'])
@token_auth.login_required
def stop_test_task(id):
    
    """
    user terminates specific test task.
    If the user is sponsor, the whole test task will be terminated.
    If the user is assistor, it will not receive any message from this test task.

    Parameters:
       test_id - String. The id of test task
       
    Returns:
        If sponsor:
            response = {
                "message": "delete successfully", 
                "isSponsor": True, 
                "cur_rounds_num": cur_rounds_num
            }
        elif assistor:
            response = {
                "message": "delete successfully", 
                "isSponsor": False, 
                "cur_rounds_num": cur_rounds_num
            }

    Raises:
        KeyError - raises an exception
    """

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    if 'test_id' not in data or not data.get('test_id'):
        return bad_request('test_id is required.')

    test_id = data.get('test_id')

    user_id = obtain_user_id_from_token()
    user_document = mongoDB.search_user_document(user_id=id,username=None, email=None, key_indicator='user_id')
    # check if the caller of the function and the id is the same
    if not verify_token_user_id_and_function_caller_id(user_id, user_document['user_id']):
        return error_response(403)

    # check if the current client is the sponsor
    isSponsor = False
    test_match_document = test_match.search_test_match_document(test_id=test_id)
    sponsor_id = test_match_document['sponsor_information']['sponsor_id']
    assistor_information = test_match_document['assistor_information']
    sponsor_information = test_match_document['sponsor_information']
    sponsor_random_id = sponsor_information[sponsor_id]['sponsor_id_to_random_id']
    asssistor_random_id_mapping = test_match_document['asssistor_random_id_mapping']
    if sponsor_id == user_id:
        isSponsor = True 

    # get recent round
    cur_rounds_num = None
    test_message_document = test_message.search_test_message_document(test_id=test_id)
    # if train_message_document is None, it means it is the first round of this train_task
    if test_message_document is None:
        cur_rounds_num = 1
    else:
        cur_rounds_num = test_message_document['cur_rounds_num']

    if isSponsor:
        # delete the stopped round in train_message Table
        # train_mongoDB.delete_rounds_in_train_message_output_document(task_id=task_id, cur_rounds_num=cur_rounds_num, role='sponsor')
        
        # put sponsor in sponsor_terminate_id_dict
        test_match.update_user_stop_in_test_match_document(test_id=test_id, user_id=user_id, role='sponsor')

        # add stop notification to all sponsor and assistors' notification table
        for assistor_id in assistor_information:
            mongoDB.update_notification_document(user_id=assistor_id, notification_name='stop_test_task', 
                                                       id=test_id, sender_random_id=sponsor_random_id, 
                                                       role='assistor', cur_rounds_num=cur_rounds_num, test_indicator='test')

        mongoDB.update_notification_document(user_id=sponsor_id, notification_name='stop_test_task', 
                                                       id=test_id, sender_random_id=sponsor_random_id, 
                                                       role='sponsor', cur_rounds_num=cur_rounds_num, test_indicator='test')
   
        response = {
            "message": "delete successfully", 
            "isSponsor": True, 
            "cur_rounds_num": cur_rounds_num
        }
    elif not isSponsor:
        # delete the stopped round in train_message Table
        # train_mongoDB.delete_rounds_in_train_message_output_document(task_id=task_id, cur_rounds_num=cur_rounds_num)
        
        # put sponsor in sponsor_terminate_id_dict
        test_match.update_user_stop_in_train_match_document(test_id=test_id, user_id=user_id, role='assistor')
        assistor_id = user_id
        assistor_random_id = asssistor_random_id_mapping[assistor_id]

        # add stop notification to its notification table
        mongoDB.update_notification_document(user_id=assistor_id, notification_name='stop_test_task', 
                                                   id=test_id, sender_random_id=assistor_random_id, 
                                                   role='assistor', cur_rounds_num=cur_rounds_num, test_indicator='test')
   
        response = {
            "message": "delete successfully", 
            "isSponsor": False, 
            "cur_rounds_num": cur_rounds_num
        }
    return jsonify(response)