from __future__ import annotations
from asyncio import Task

"""
colda
~~~~~~

The colda package - a Python package template project that is intended
to be used as a cookie-cutter for developing new Python packages.
"""
# import os
# basedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'Algorithm')
# print("--", basedir)
# import sys
# sys.path.append(basedir)
import os
import sys
import time
import errno
import pickle
import requests
# import Algorithm

# import colda

from colda.authentication.api import Authentication
from colda.short_polling.api import ShortPolling
from colda.database.strategy.api import DatabaseOperator
from colda.network.api import Network
from colda.pi.api import PI

from colda.algorithm.strategy.custom.api import (
    GetTrainFixedParameter,
    GetTrainOptimizedParameter,
    GetTrainOwnFunction,
    GetTestFixedParameter,
    GetTestOptimizedParameter,
    GetTestOwnFunction
)

from colda.algorithm.strategy.api import (
    TrainAlgorithm,
    TestAlgorithm
)

from colda.workflow.api import (
    TrainMainWorkflow,
    TestMainWorkflow
)

from colda.utils.log.api import (
    GetAlgorithmLog,
    GetWorkflowLog,
)

from typing import (
    Callable
)

from colda._typing import (
    Mode,
    Task_Mode,
    Model_Name,
    Metric_Name
)
    
_default_train_algo = TrainAlgorithm.get_instance()
_default_test_algo = TestAlgorithm.get_instance()
_default_network = Network.get_instance()
_default_PI = PI.get_instance()
_default_DatabaseOperator = DatabaseOperator.get_instance()
_default_authentication = Authentication.get_instance()
_default_TrainMainWorkflow = TrainMainWorkflow.get_class()
_default_TestMainWorkflow = TestMainWorkflow.get_class()
_default_ShortPolling = ShortPolling.get_instance()
_default_network = Network.get_instance()
_default_PI = PI.get_instance()
_default_algo_log = GetAlgorithmLog.get_instance()
_default_workflow_log = GetWorkflowLog.get_instance()

from colda.database.api import (
    get_all_train_id_as_sponsor,
    get_all_test_id_as_sponsor,
    get_all_train_id_as_assistor,
    get_all_test_id_as_assistor,
    get_all_train_id,
    get_all_test_id
)

from colda.algorithm.api import (
    get_algo_log,
    get_all_algo_logs
)


def handle_process_exception(args):
    _default_ShortPolling.shortpolling['running'] = False
    print('handle_exception')

sys.excepthook = handle_process_exception

def test_function() -> str:
    return 'test successfully'


def register(
    username: str, 
    email: str, 
    password: str
) -> None:
    '''
    User registers.

    Parameters
    ----------
    username : str
    email : str
    password : str

    Returns
    -------
    None
    '''
    _default_authentication.user_register(
        username=username, 
        email=email,
        password=password
    )
    return
    
def login(
    username: str, 
    password: str
) -> bool:
    '''
    User login.

    Parameters
    ----------
    username : str
    password : str

    Returns
    -------
    None
    '''
    _default_authentication.user_login(
        username=username, 
        password=password
    )
    return

def logout():
    '''
    User logout.

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    return _default_authentication.user_logout()

def call_for_train(
    max_round: int, 
    assistors: list, 
    task_mode: Task_Mode, 
    model_name: Model_Name, 
    metric_name: Metric_Name,
    train_file_path: str, 
    train_id_column: str, 
    train_data_column: str, 
    train_target_column: str, 
    task_name: str=None, 
    task_description: str=None
) -> None:
    '''
    Sponsor initiate a new training 
    task.

    Parameters
    ----------
    max_round : int
    assistors : list
    task_mode : Task_Mode
    model_name : Model_Name
    metric_name : Metric_Name
    train_file_path : str
    train_id_column : str
    train_data_column : str
    train_target_column : str
    task_name : str=None
    task_description : str=None

    Returns
    -------
    None
    '''
    _default_TrainMainWorkflow.find_assistor(
        max_round=max_round, 
        assistors=assistors, 
        task_mode=task_mode, 
        model_name=model_name, 
        metric_name=metric_name, 
        train_file_path=train_file_path, 
        train_id_column=train_id_column, 
        train_data_column=train_data_column, 
        train_target_column=train_target_column, 
        task_name=task_name, 
        task_description=task_description
    )
    return 
    

def call_for_test(
    train_id: str, 
    test_file_path: str, 
    test_id_column: str, 
    test_data_column: str, 
    test_target_column: str, 
    test_name: str=None, 
    test_description: str=None
) -> None:
    '''
    Sponsor call for test of a
    train task.

    Parameters
    ----------
    train_id : str
    test_file_path : str
    test_id_column : str 
    test_data_column : str
    test_target_column : str 
    test_name : str=None 
    test_description : str=None

    Returns
    -------
    None
    '''
    _default_TestMainWorkflow.find_test_assistor(
        train_id=train_id, 
        test_file_path=test_file_path, 
        test_id_column=test_id_column, 
        test_data_column=test_data_column, 
        test_target_column=test_target_column, 
        test_name=test_name, 
        test_description=test_description
    )
    return

def start_cooperation() -> None:
    '''
    Start cooperation

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    # print(f'?iddd: {id(_default_ShortPolling)}')
    _default_ShortPolling.start_cooperation()
    return

def end_cooperation() -> None:
    '''
    End cooperation

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    _default_ShortPolling.end_cooperation()
    return

def set_default_info(
    default_mode: Mode, 
    default_task_mode: Task_Mode, 
    default_model_name: Model_Name, 
    default_file_path: str=None, 
    default_id_column: str=None, 
    default_data_column: str=None
) -> None:
    '''
    Set default info used for training and
    testing as assistor.

    Parameters
    ----------
    default_mode : Mode
    default_task_mode : Task_Mode
    default_model_name : Model_Name 
    default_file_path : str=None 
    default_id_column : str=None
    default_data_column : str=None

    Returns
    -------
    None
    '''
    PI_instance = PI.get_instance()
    user_id = PI_instance.user_id
    if user_id == None:
        return 'Please Login first'
    PI_instance.default_mode = default_mode
    _default_DatabaseOperator.set_database(database_type='default_metadata')
    return _default_DatabaseOperator.store_record(
        user_id=user_id, 
        default_mode=default_mode, 
        default_task_mode=default_task_mode, 
        default_model_name=default_model_name,
        default_file_path=default_file_path, 
        default_id_column=default_id_column, 
        default_data_column=default_data_column
    )

def store_database(path, mode='pickle'):
    dirname = os.path.dirname(path)
    input = _default_database
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise
    if mode == 'pickle':
        pickle.dump(input, open(path, 'wb'))
    else:
        raise ValueError('Not valid save mode')
    return True




# https://juejin.cn/post/6844903503660335112
def set_train_stage_custom_handler(
    handler_type: str = 'fixedParameter',
    OwnFunction: dict[str, Callable] = None
):

    if handler_type == 'fixedParameter':
        custom = GetTrainFixedParameter.get_class()
    elif handler_type == 'optimizerTrainedParameter':
        custom = GetTrainOptimizedParameter.get_class()
    elif handler_type == 'ownFunctionParameter':
        GetTrainOwnFunction.get_class().OwnFunction = OwnFunction
        custom = GetTrainOwnFunction.get_class()

    _default_train_algo.train_custom = custom
    return


def set_test_stage_custom_handler(
    handler_type: str = 'fixedParameter', 
    OwnFunction: dict[str, Callable] = None
):

    if handler_type == 'fixedParameter':
        custom = GetTestFixedParameter.get_instance()
    elif handler_type == 'optimizerTrainedParameter':
        custom = GetTestOptimizedParameter.get_instance()
    elif handler_type == 'ownFunctionParameter':
        GetTestOwnFunction.get_class().OwnFunction = OwnFunction
        custom = GetTestOwnFunction.get_class()
    
    _default_test_algo.test_custom = custom
    return


def get_pending_requests():
    pass
    
def get_online_user(username: list):
    pass

# def test_function():
#     return 'test successfully' 
# # userLogin("xie2", "Xie2@123")
# # set_default_data_path("/Users/qile/Documents/data/BostonHousing/2/123/0.5/0/train/data.csv", "1", "2")
# # callForTrain(2, [2], "/Users/qile/Documents/data/combine.csv", "1", "2-7", "8")



