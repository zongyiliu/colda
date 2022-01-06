import { login_helper } from './helper_folder/Apollo_login_helper';
import { find_assistor_helper } from './helper_folder/Apollo_find_assistor_helper'
import { profile_helper } from './helper_folder/Apollo_profile_helper'
// import { unread_request_helper } from './helper_folder/Apollo_unread_request_helper'
import {  unittest_parameters,  modify_parameter, Navbar_wrapper } from './helper_folder/Apollo_unittest_init'
// import {  get_notifications, update_notifications } from './helper_folder/Apollo_unittest_utils'
import { unread_request_helper } from './helper_folder/Apollo_unread_request_helper';
import axios from 'axios';
import { notification_helper } from './helper_folder/Apollo_notification_helper';
import { delete_db_helper } from './helper_folder/Apollo_delete_db_helper'
import { logout_helper} from './helper_folder/Apollo_logout_helper'
// import store from '../../src/store'
jest.setTimeout(10000);





afterAll(() => {
  window.localStorage.setItem('Apollo-token', null)
  console.log('afterAll')
});

describe('test_unread_request', () => {
  console.log('des1')

// }
  // Sponsor logins
  login_helper.check_login_first_user()
  delete_db_helper.delete_db()
  // Sponsor gets train id
  find_assistor_helper.get_train_id()
  // Sponsor finds assistor
  find_assistor_helper.onSubmit()
  logout_helper.logout()

  // Assistor logins
  // window.localStorage.removeItem('Apollo-token')
  // store.state.is_authenticated = false
  // store.state.user_id = 0
  // login_helper.check_login_second_user()
  // // Assistor updates default_train_file_path, default_train_id_column, 
  // // default_train_data_column
  // profile_helper.onSubmit()

  
  // notification_helper.update_notification()
  // // console.log('rsee')
  // unread_request_helper.unread_request()
  // logout_helper.logout()
 

})
