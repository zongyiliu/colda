from __future__ import annotations

import requests

from synspot.workflow.train_base import TrainBaseWorkflow

from synspot.utils import(
    ParseJson
)

from synspot.workflow.utils import (
    obtain_notification_information
)

from typing import Any


class TrainSponsorSituation(TrainBaseWorkflow):
    __role = 'sponsor'

    @classmethod
    def train_sponsor_situation(
            cls, train_id: str, train_id_dict: dict[str, Any]
        ) -> None:

        msgs = [
            "---- 4. Unread Situation", 
            "4.1 Update the situation notification"
        ]
        cls._store_log(
            user_id=user_id,
            task_id=train_id,
            msgs=msgs
        )

        user_id, root, token = cls._get_important_information()
        sender_random_id, role, cur_rounds_num = obtain_notification_information(notification_dict=train_id_dict)

        msgs = [
            f'4.2 Current round is: {cur_rounds_num}'
        ]
        cls._store_log(
            user_id=user_id,
            task_id=train_id,
            msgs=msgs
        )

        sponsor_metadata_record = cls._get_database_record(
            database_type='train_sponsor_metadata',
            user_id=user_id,
            train_id=train_id
        )
        task_mode = sponsor_metadata_record[0]
        model_name = sponsor_metadata_record[1]
        metric_name = sponsor_metadata_record[2]
        train_file_path = sponsor_metadata_record[3]
        train_id_column = sponsor_metadata_record[4]
        train_data_column = sponsor_metadata_record[5]
        train_target_column = sponsor_metadata_record[6]
        task_name = sponsor_metadata_record[7]
        task_description = sponsor_metadata_record[8]

        sponsor_residual = cls._get_database_record(
            database_type='train_algorithm',
            user_id=user_id,
            train_id=train_id,
            algorithm_data_name='sponsor_residual'
        )

        # train cooperative model using residual of current round as target
        trained_cooperative_model, trained_cooperative_model_output = cls._train_cooperative_model(
            dataset_path=train_file_path, 
            data_idx=train_data_column, 
            skip_header=cls._skip_header, 
            task_mode=task_mode, 
            model_name=model_name,
            cur_round_residual=sponsor_residual,
            role=cls.__role,
            matched_identifier=None,
        )

        # Store trained_cooperative_model for further testing
        cls._store_database_record(
            database_type='train_algorithm',
            user_id=user_id,
            train_id=train_id,
            algorithm_data_name=f'trained_cooperative_model_rounds_{cur_rounds_num}',
            algorithm_data=trained_cooperative_model
        )

        # Store trained_cooperative_model_output for calculating result
        cls._store_database_record(
            database_type='train_algorithm',
            user_id=user_id,
            train_id=train_id,
            algorithm_data_name='trained_cooperative_model_output',
            algorithm_data=trained_cooperative_model_output
        )

        msgs = [
            f'4.3 Sponsor round {cur_rounds_num} training done',
            '---- 4. Unread Situation Done'
        ]
        cls._store_log(
            user_id=user_id,
            task_id=train_id,
            msgs=msgs
        )

        print('Sponsor: Training train_id: ', train_id, ' is running')
        return True
