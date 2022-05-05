from __future__ import annotations

import time
import threading
from urllib import request
from synspot.network import Network
from synspot.personalinformation import PersonalInformation
from synspot.utils.log import GetWorkflowLog
from synspot.algorithm.strategy import BaseAlgorithmStrategy

from synspot.database.strategy import DatabaseOperator

from synspot._typing import (
    Train_Database_Type,
    Test_Database_Type
)

import warnings

from synspot.error import (
    StatusCodeWarning,
    StatusCodeError
)

from typing import (
    final,
    Union,
    Any,
    Final,
)


class BaseWorkflow:
    _skip_header: Final[int] = 1
    _initial_round_num: Final[int] = 1
    _url_prefix: Final[str] = 'main_flow'
    _maxRound: Final[int] = 3

    __Network_instance = Network.get_instance()
    __PersonalInformation_instance = PersonalInformation.get_instance()
    
    __DatabaseOperator_instance = DatabaseOperator.get_instance()
    __BaseAlgorithm_instance = BaseAlgorithmStrategy()

    __log = GetWorkflowLog.get_log()

    @final
    @classmethod
    def _get_important_information(cls) -> tuple[str, str, str]:
        """
        Obtain the information we need: user_id, root, token, task_id

        :param get_train_id: Boolean. Indicate if we need to get the new train id

        :returns: A tuple of ``(user_id, root, token, task_id)``

        :exception OSError: Placeholder.
        """
        user_id = cls.__PersonalInformation_instance.user_id
        # assert user_id is not None
        root = cls.__PersonalInformation_instance.root
        # assert root is not None
        token = cls.__Network_instance.token
        # assert token is not None
        return user_id, root, token
    
    @final
    @classmethod
    def _get_default_mode(cls) -> str:
        return cls.__PersonalInformation_instance.default_mode
    
    @final
    @classmethod
    def _get_request_chaining(
        cls, 
        task_id: str,
        url_prefix: str,
        url_root: str,
        url_suffix: str,
        status_code: int,
    ) -> dict[str, Union(list[str], str)]:

        request_response = cls.__Network_instance.get_request_chaining(
            url_prefix=url_prefix,
            url_root=url_root,
            url_suffix=url_suffix,
            status_code=status_code,
        )

        if request_response == StatusCodeError:
            warnings.warn(
            f"{task_id}'s network get request to {url_root} goes wrong", 
            StatusCodeWarning
        )
        
        return request_response

    @final
    @classmethod
    def _post_request_chaining(
        cls, 
        task_id: str,
        data: dict[str, Union(list[str], str)],
        url_prefix: str,
        url_root: str,
        url_suffix: str,
        status_code: int,
    ) -> dict[str, Union(list[str], str)]:

        return cls.__Network_instance.post_request_chaining(
            data=data,
            url_prefix=url_prefix,
            url_root=url_root,
            url_suffix=url_suffix,
            status_code=status_code
        )

    @final
    @classmethod
    def _store_log(
        cls,
        user_id: str,
        task_id: str,
        msgs: list[str],
    ) -> None:

        cls.__log.store_log(
            user_id=user_id,
            task_id=task_id,
            msgs=msgs
        )
        return None

    @final
    @classmethod
    def _store_database_record(
        cls,
        database_type: Union(Train_Database_Type, Test_Database_Type),
        **kwargs,
    ) -> None:

        cls.__DatabaseOperator_instance.set_database(
            database_type=database_type
        )

        cls.__DatabaseOperator_instance.store_record(
            **kwargs
        )
        
        return 
    
    @final
    @classmethod
    def _get_database_record(
        cls,
        database_type: Union(Train_Database_Type, Test_Database_Type),
        **kwargs,
    ) -> tuple[Any]:

        cls.__DatabaseOperator_instance.set_database(
            database_type=database_type
        )

        return cls.__DatabaseOperator_instance.get_record(
            **kwargs
        )

    @final
    @classmethod
    def _encrypt_identifier(
        cls,
        dataset_path: str,
        id_idx: str,
        skip_header: int
    ) -> None:

        encrypted_identifer = cls.__BaseAlgorithm_instance.make_hash(
                # self_id=user_id, 
                # train_id=train_id, 
                # mode=self.test_indicator, 
                # test_id=None, 
                dataset_path=dataset_path, 
                id_idx=id_idx, 
                skip_header=skip_header
            )
        return encrypted_identifer
    
    @final
    @classmethod
    def _match_identifier(
        cls,
        self_id_data: list[str],
        from_id_data: list[str]
    ) -> list[str]:

        matched_identifier = cls.__BaseAlgorithm_instance.make_match_idx(
            self_id_data=self_id_data,
            from_id_data=from_id_data
        )
        return matched_identifier

    @final
    @classmethod
    def _async_checker(
        cls,
        database_type: str,
        user_id: str,
        train_id: str,
        algorithm_data_name: str,
        waiting_start_time: type[time.time()]
    ) -> bool:

        if not cls._get_database_record(
            database_type=database_type,
            user_id=user_id,
            train_id=train_id,
            algorithm_data_name=algorithm_data_name
        ):

            waiting_current_time = time.time()
            time_interval = waiting_current_time - waiting_start_time
            if time_interval > 30 * 60:
                print('Sorry, the test stopped due to slow computation')
                return False

            args = [
                database_type,
                user_id,
                train_id,
                algorithm_data_name,
                waiting_start_time
            ]
            threading.Timer(
                30, 
                cls._async_checker, 
                args)

        return True

    

