# -*- coding: utf-8 -*-
import re
from operator import itemgetter
from flask import Flask, session, request, g, current_app, render_template, flash
from flask.helpers import url_for
from flask.json import jsonify

# from Items import db
from Items import pyMongo
from flask_cors import CORS, cross_origin
# import BluePrint
from Items.main import main
from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

# from Items.models import User, Notification, Message
from Items.main.errors import bad_request, error_response
from Items.main.auth import token_auth, basic_auth
from Items.main.utils import obtain_user_id_from_token, obtain_unique_id
from Items.main.utils import log, generate_msg, validate_password, send_email, generate_confirmation_token, confirm_token
from Items.main.utils import generate_password, check_password, verify_token_user_id_and_function_caller_id

from Items.main.mongoDB import mongoDB

@main.route('/users', methods=['POST'])
def create_user():

    """
    Register new user

    Parameters:
        username - String. The id of task
        email - String. The matching id file sent by sponsor
        password - String.

    Returns:
        data - Dict. { task_id - String: The id of task, assistor_num - Integer: The number of assistors in this task }

    Raises:
        KeyError - raises an exception
    """

    data = request.get_json()
    if not data:
      return bad_request('No data. Please import JSON data')

    message = {}
    if 'username' not in data or not data.get('username', None) or (' ' in data.get('username')):
        message['username'] = 'Please provide a valid username.'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)) or (' ' in data.get('email')):
        message['email'] = 'Please provide a valid email address.'
    if 'password' not in data or not data.get('password', None) or (' ' in data.get('password')):
        message['password'] = 'Please provide a valid password.'
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    password_hash = generate_password(password)

    user_document = pyMongo.db.User.find_one({'username': username})
    if user_document:
        message['username'] = 'Please use a different username.'
    user_document = pyMongo.db.User.find_one({'email': email})
    if user_document:
        message['email'] = 'Please use a different email address.'
    
    validate_password_indicator, return_message = validate_password(password)
    print('register', validate_password_indicator, return_message)
    if not validate_password_indicator:
        message['password'] = return_message
    if message:
        return bad_request(message)
    
    newObjectId = ObjectId()
    user_document = {
        '_id': newObjectId,
        'user_id': str(newObjectId),
        'username': username,
        'email': email,
        'password_hash': password_hash,
        'name': None,
        'location': None,
        'about_me': None,
        'authority_level': 'user',
        'confirm_email': False,
        'participated_train_task': {},
    }
    pyMongo.db.User.insert_one(user_document)

    token = generate_confirmation_token(email)
    confirm_url = url_for('main.confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(email, subject, html)

    return_dict = {}
    return_dict['token'] = token
    return_dict['message'] = 'create successfully'
    response = jsonify(return_dict)
    response.status_code = 201
    return response

@main.route('/confirm_email/<token>', methods=['GET'])
def confirm_email(token):

    """
    Confirm the link in the email 

    Parameters:
       token - instance of URLSafeTimedSerializer.
       
    Returns:
        msg - String. Depends on different situation

    Raises:
        KeyError - raises an exception
    """

    email = confirm_token(token)
    user = pyMongo.db.User.find_one({'email': email})

    msg = ''
    if user:
        if user['confirm_email'] == False:
            if user['email'] == email:
                pyMongo.db.User.update_one({'email': email}, {'$set':{
                    'confirm_email': True
                }})
                msg = 'You have confirmed your account. Thanks!'
            else:
                msg = 'The confirmation link is invalid or has expired.'
        else:
            msg = 'Account already confirmed. Please login.'
    else:
        msg = 'The confirmation link is invalid or has expired.'

    return render_template('confirm.html', msg=msg)

@main.route('/resend/', methods=['POST'])
def resend():
    
    """
    Resend the email link

    Parameters:
        username - String.
       
    Returns:
        'Resend successfully!'

    Raises:
        KeyError - raises an exception
    """

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    if 'username' not in data or not data.get('username'):
        return bad_request('username is required.')

    username = data.get('username')

    user_document = mongoDB.search_user_document(user_id=None, username=username)
    email = user_document['email']

    token = generate_confirmation_token(email)
    confirm_url = url_for('main.confirm_email', token=token, _external=True)
    html = render_template('activate.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(email, subject, html)

    response = {
        'message': 'Resend successfully!'
    }
    return jsonify(response)

@main.route('/forgot', methods=['POST'])
def forgot():
    
    """
    Reset the password

    Parameters:
        username - String.
        email - String.
       
    Returns:
        'A password reset email has been sent via email.'

    Raises:
        KeyError - raises an exception
    """

    data = request.get_json()
    message = {}
    if 'username' not in data or not data.get('username', None):
        message['username'] = 'Please provide a valid username.'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)):
        message['email'] = 'Please provide a valid email address.'
    
    username = data.get('username')
    email = data.get('email')

    user_document = mongoDB.search_pending_document(user_id=None, username=username)
    if not user_document:
        message['username'] = 'Please type in the correct username.'
    if user_document['email'] != email:
        message['email'] = 'Please type in the correct username and email'
        message['username'] = 'Please type in the correct username and email'
    if message:
        return bad_request(message)

    token = generate_confirmation_token(email)
    reset_url = url_for('main.forgot_new', token=token, _external=True)
    html = render_template('reset.html',
                            username=username,
                            reset_url=reset_url)
    subject = "Reset your password"
    send_email(email, subject, html)

    response = {
        'message': 'A password reset email has been sent via email.'
    }
    return jsonify(response)


@main.route('/forgot/new/<token>', methods=['GET', 'POST'])
def forgot_new(token):

    """
    backend function to handle resetting the password

    Parameters:
        username - String.
        email - String.
       
    Returns:
        'A password reset email has been sent via email.'

    Raises:
        KeyError - raises an exception
    """

    if request.method == 'POST':
        # would have a "\" append in the end
        token = request.form['token'][:-1]

    email = confirm_token(token)
    if email == False:
        flash('Token has expired')
        return 'Token has expired'

    # form = ChangePasswordForm()
    # if form.validate_on_submit():
    user_document = pyMongo.db.User.find_one({'email': email})
    if not user_document:
        flash('Cannot Find the User according to email')
        return 'Cannot Find the User according to email'
    
    if request.method == 'POST':
 
        password = request.form['newPassword']

        validate_password_indicator, return_message = validate_password(password)
        if not validate_password_indicator:
            msg = ('New password must follow the following instructions:\n' + ' At least 8 characters. At most 25 characters\n'
                + 'A mixture of both uppercase and lowercase letters\n' + 'A mixture of letters and numbers' + 'Inclusion of at least one special character, e.g., ! @')
            confirm_url = url_for('main.forgot_new', token=token, msg=msg, _external=True)
            return render_template('forgot_new.html', confirm_url=confirm_url)

 
        user_password_hash = generate_password_hash(password)
        pyMongo.db.User.update_one({'email': email}, {'$set':{
            'password_hash': user_password_hash
        }})

        flash('Password successfully changed.')
        return 'Password successfully changed.'
    else:
        print('123token', token)
        msg = 'Hello ' + user_document['username']
        confirm_url = url_for('main.forgot_new', token=token, _external=True)
        print("/forgot/new/<token>_confirm_url", confirm_url)
        return render_template('forgot_new.html', confirm_url=confirm_url, msg=msg, token=token)

@main.route('/users/<string:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):

    """
    Get information of user itself

    Parameters:
        id - String. user id queried by the function caller
       
    Returns:
        Dict or None

    Raises:
        KeyError - raises an exception
    """

    user_id = obtain_user_id_from_token()
    if verify_token_user_id_and_function_caller_id(user_id, id):
        response = {
            'user': g.current_user
        }
        return jsonify(response)
    return None

@main.route('/users/<string:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):

    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data.')
    elif 'username' not in data or not data.get('username', None) or (' ' in data.get('username')):
        message['username'] = 'Please provide a valid username.'
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, data.get('email', None)) or (' ' in data.get('email')):
        message['email'] = 'Please provide a valid email address.'

    user_id = obtain_user_id_from_token()
    user_document = mongoDB.search_user_document(user_id=id,username=None, email=None, key_indicator='user_id')
    # check if the caller of the function and the id is the same
    if not verify_token_user_id_and_function_caller_id(user_id, user_document['user_id']):
        return error_response(403)

    username = data.get('username')
    email = data.get('email')
    
    message = {}
    if mongoDB.search_user_document(user_id=None, username=username):
        message['username'] = 'Please use a different username.'
    if pyMongo.db.User.find_one({'email': email}):
        message['email'] = 'Please use a different email address.'

    if message:
        return bad_request(message)

    response = {

    }
    return jsonify(response)


@main.route('/users/<string:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    '''
      Delete a User. Implement Later
    '''
    return "Welcome to Delete!"


# @main.route('/users/<string:id>/history-messages/', methods=['GET'])
# @token_auth.login_required
# def get_user_history_messages(id):
#     '''返回我与某个用户(由查询参数 from 获取)之间的所有私信记录'''
#     user_id = obtain_user_id_from_token()
#     user_document = mongoDB.search_user_document(user_id=id,username=None, email=None, key_indicator='user_id')
#     # check if the caller of the function and the id is the same
#     if not verify_token_user_id_and_function_caller_id(user_id, user_document['user_id']):
#         return error_response(403)

#     page = request.args.get('page', 1, type=int)
#     per_page = min(
#         request.args.get(
#             'per_page', current_app.config['MESSAGES_PER_PAGE'], type=int), 100)
#     from_id = request.args.get('from', type=int)

#     if not from_id:  # 必须提供聊天的对方用户的ID
#         return bad_request('You must provide the user id of opposite site.')
#     # 对方发给我的
#     q1 = Message.query.filter(Message.sender_id == from_id, Message.recipient_id == id)
#     # 我发给对方的
#     q2 = Message.query.filter(Message.sender_id == id, Message.recipient_id == from_id)
#     # 按时间正序排列构成完整的对话时间线
#     history_messages = q1.union(q2).order_by(Message.timestamp)
#     data = Message.to_collection_dict(history_messages, page, per_page, 'main.get_user_history_messages', id=id)
#     # print("page",page,"length",len(data['items']))
#     # 现在这一页的 data['items'] 包含对方发给我和我发给对方的
#     # 需要创建一个新列表，只包含对方发给我的，用来查看哪些私信是新的
#     recived_messages = [item for item in data['items'] if item['sender']['id'] != id]
#     sent_messages = [item for item in data['items'] if item['sender']['id'] == id]
#     # 然后，标记哪些私信是新的
#     last_read_time = user.last_messages_read_time or datetime(1900, 1, 1)
#     new_count = 0
#     for item in recived_messages:
#         if item['timestamp'] > last_read_time:
#             item['is_new'] = True
#             new_count += 1
#     if new_count > 0:
#         # 更新 last_messages_read_time 属性值为收到的私信列表最后一条(最近的)的时间
#         user.last_messages_read_time = recived_messages[-1]['timestamp']
#         db.session.commit()  # 先提交数据库，这样 user.new_recived_messages() 才会变化
#         # 更新用户的新私信通知的计数
#         user.add_notification('unread_messages_count', user.new_recived_messages())
#         db.session.commit()
#     # 最后，重新组合 data['items']，因为收到的新私信添加了 is_new 标记
#     messages = recived_messages + sent_messages
#     messages.sort(key=data['items'].index)  # 保持 messages 列表元素的顺序跟 data['items'] 一样
#     data['items'] = messages
#     return jsonify(data)
