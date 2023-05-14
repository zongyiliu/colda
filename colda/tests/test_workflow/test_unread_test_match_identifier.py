"""
tests.test_curves.py
~~~~~~~~~~~~~~~~~~~~

Test suite for the curves.py module that handles everything to do with
supply and demand curves.
"""
import pytest
from .__init__ import (
    testing_data,
    Regression_1s_1a
)

from .Train_helper_function import Train_helper_function
from .Test_helper_function import Test_helper_function

# from workflow.base import BaseWorkflow

# from tests.test_workflow.conftest import Regression_1s_1a_strategy

class Test_unread_test_match_identifier(Train_helper_function, Test_helper_function):

        # @pytest.mark.usefixtures('Regression_1s_1a_strategy')
        @pytest.mark.parametrize("unittest_strategy", [
            Regression_1s_1a,
        ])
        def test_unread_test_match_identifier(self, unittest_strategy):
            
            testing_data['max_round'] = 1
            # BaseWorkflow._max_round = 1
            super().first_user_login()
            super().clean_db()
            train_id = super().find_assistor()

            # unread_request
            super().second_user_login()
            super().set_default_information()
            notification_category = self.get_notification()
            print('5555', notification_category)
            assert "unread_request" in notification_category.keys()
            super().train_assistor_request(notification_category)
            
            # unread_match_identifier_assistor
            super().second_user_login()
            notification_category = self.get_notification()
            print('666', notification_category)
            assert "unread_match_identifier" in notification_category.keys()
            super().train_assistor_match_identifier(notification_category)

            # unread_match_identifier_sponsor
            super().first_user_login()
            notification_category = self.get_notification()
            print('77', notification_category)
            assert "unread_match_identifier" in notification_category.keys()
            super().train_sponsor_match_identifier(notification_category)

            # unread_sponsor_situation
            super().first_user_login()
            notification_category = self.get_notification()
            print('88', notification_category)
            assert "unread_situation" in notification_category.keys()
            super().train_sponsor_situation(notification_category)

            # unread_assistor_situation
            super().second_user_login()
            notification_category = self.get_notification()
            print('99', notification_category)
            assert "unread_situation" in notification_category.keys()
            super().train_assistor_situation(notification_category)

             # unread_sponsor_output
            super().first_user_login()
            notification_category = self.get_notification()
            print('1010', notification_category)
            assert "unread_output" in notification_category.keys()
            super().train_output(notification_category)

            super().first_user_login()
            test_id = super().find_test_assistor(train_id=train_id)

            super().second_user_login()
            notification_category = self.get_notification()
            print('1111', notification_category)
            assert "unread_test_request" in notification_category.keys()
            super()._test_assistor_request(notification_category)

            # unread_match_identifier_sponsor
            super().first_user_login()
            notification_category = self.get_notification()
            print('1313', notification_category)
            assert "unread_test_match_identifier" in notification_category.keys()
            print('%$!@$!@#!@', unittest_strategy)
            super()._test_sponsor_match_identifier(
                notification_category=notification_category, 
                unittest_strategy=unittest_strategy,
                user_id=super().get_user_id(),
                test_id=test_id
            )

            # unread_match_identifier_assistor
            super().second_user_login()
            notification_category = self.get_notification()
            print('1212', notification_category)
            assert "unread_test_match_identifier" in notification_category.keys()
            super()._test_assistor_match_identifier(
                notification_category=notification_category, 
                unittest_strategy=unittest_strategy,
                user_id=super().get_user_id(),
                test_id=test_id
            )

            
