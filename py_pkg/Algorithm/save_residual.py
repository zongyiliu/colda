import os
from algo_utils import makedir_exist_ok


def save_residual(root, self_id, task_id, round):
    # root = args['root']
    # self_id = args['self_id']
    # task_id = args['task_id']
    # round = args['round']
    residual_path = os.path.join(root, self_id, 'task', task_id, 'train', 'round', str(round), 'residual')
    makedir_exist_ok(residual_path)
    open(os.path.join(residual_path, '{}.csv'.format(self_id)), "a")
    residual_path = os.path.join(residual_path, '{}.csv'.format(self_id))
    return '200?save_residual?{}'.format(residual_path)
