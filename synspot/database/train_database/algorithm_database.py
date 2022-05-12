from __future__ import annotations

import collections

from synspot.database.base import BaseDatabase

from synspot.database.abstract_database import AbstractAlgorithmDatabase

from synspot.utils import DictHelper

from typing import (
    Union,
    Any
)


class TrainAlgorithmDatabase(BaseDatabase, AbstractAlgorithmDatabase):
    __TrainAlgorithmDatabase_instance = None

    def __init__(self):
        self.__temp_database = collections.defaultdict(dict)

    @classmethod
    def get_instance(cls) -> type[TrainAlgorithmDatabase]:
        if cls.__TrainAlgorithmDatabase_instance == None:
            cls.__TrainAlgorithmDatabase_instance = TrainAlgorithmDatabase()

        return cls.__TrainAlgorithmDatabase_instance

    def get_all_records(self) -> list[tuple[str, str]]:
        return DictHelper.get_all_key_value_pairs(container=self.__temp_database)

    def store_record(
        self, 
        user_id: str, 
        train_id: str, 
        algorithm_data_name: str,
        algorithm_data: Union(list[str], list[list[str]], Any),
    ) -> None:
        
        """
        start task with all assistors

        :param maxRound: Integer. Maximum training round
        :param assistors: List. The List of assistors' usernames

        :returns: Tuple. Contains a string 'handleTrainRequest successfully' and the task id

        :exception OSError: Placeholder.
        """

        key = DictHelper.generate_dict_key(user_id, train_id, algorithm_data_name)
        # if key not in self.__temp_database:
        #     self.__temp_database[key] = collections.defaultdict(dict)
        print('***', key)
        temp_key = str(key)

        store_res = DictHelper.store_value(
            key=key,
            value=algorithm_data,
            container=self.__temp_database,
            store_type='multiple_access'
        )
        if store_res == True:
            return f'{self.__class__.__name__} stores {temp_key} successfully!' 
        else:
            return store_res
    
    def get_record(
        self, 
        user_id: str, 
        train_id: str, 
        algorithm_data_name: str,
    ) -> None:
        
        """
        start task with all assistors

        :param maxRound: Integer. Maximum training round
        :param assistors: List. The List of assistors' usernames
        :param train_file_path: String. Input path address of training data path
        :param train_id_column: String. ID column of Input File
        :param train_data_column: String. Data column of Input File
        :param train_target_column: String. Target column of Input File
        :param task_mode: String. Classification or Regression
        :param model_name: String. Specific model, such as LinearRegression, DecisionTree.
        :param metric_name: String. Metric to measure the result, such as MAD, RMSE, R2.
        :param task_name: None or String. The name of current task.
        :param task_description: None or String. The description of current task

        :returns: Tuple. Contains a string 'handleTrainRequest successfully' and the task id

        :exception OSError: Placeholder.
        """

        if not train_id:
            raise RuntimeError('Use train_id to retrieve User_Assistor_Table')
        if not algorithm_data_name:
            print('placeholder')
            
        key = DictHelper.generate_dict_key(user_id, train_id, algorithm_data_name)
        # if key not in self.__temp_database:
        #     print(f'{self.__class__.__name__} does not contain the record')
        #     return '666666'

        algorithm_data = DictHelper.get_value(
            key=key,
            container=self.__temp_database
        )
        
        if not super().if_db_response_valid(
            algorithm_data, 
        ):
            print(f'{self.__class__.__name__} does not contain the record')
            return super().dict_value_not_found()

        return algorithm_data
       
   