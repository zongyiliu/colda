import pytest
from synspot.tests.test_database.conftest import DatabaseOperator_instance

class TestTrainAlgorithmDatabase:

    @pytest.mark.usefixtures('DatabaseOperator_instance')
    @pytest.mark.parametrize("test_record, expected_res", [
        (('test', 'test', 'test1', ''), "TrainAlgorithmDatabase stores ('test', 'test') successfully!"),
        (('test', 'test', 'test2', 'test'), "TrainAlgorithmDatabase stores ('test', 'test') successfully!")
    ])
    def test_store_record(self, DatabaseOperator_instance, test_record, expected_res):
        DatabaseOperator_instance.set_database(database_type='train_algorithm')
        response = DatabaseOperator_instance.store_record(
            user_id=test_record[0], 
            train_id=test_record[1], 
            algorithm_data_name=test_record[2],
            algorithm_data=test_record[3]
        )
        assert response == expected_res

    
    @pytest.mark.usefixtures('DatabaseOperator_instance')
    @pytest.mark.parametrize("test_record, expected_res", [
        (('test', 'test', 'test1'), ''),
        (('test', 'test', 'test2'), 'test')
    ])
    def test_get_record(self, DatabaseOperator_instance, test_record, expected_res):
        response = DatabaseOperator_instance.get_record(
            user_id=test_record[0], 
            train_id=test_record[1], 
            algorithm_data_name=test_record[2],
        )
        assert response == expected_res