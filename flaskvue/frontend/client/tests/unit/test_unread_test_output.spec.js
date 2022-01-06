import { login_helper } from './helper_folder/Apollo_login_helper';
import { find_test_assistor_helper } from './helper_folder/Apollo_find_test_assistor_helper'
import { profile_helper } from './helper_folder/Apollo_profile_helper'
// import { unread_request_helper } from './helper_folder/Apollo_unread_request_helper'
import {  unittest_parameters,  modify_parameter, Navbar_wrapper } from './helper_folder/Apollo_unittest_init'
// import {  get_notifications, update_notifications } from './helper_folder/Apollo_unittest_utils'
import { unread_test_request_helper } from './helper_folder/Apollo_unread_test_request_helper';
import axios from 'axios';
import { notification_helper } from './helper_folder/Apollo_notification_helper';
import { logout_helper } from './helper_folder/Apollo_logout_helper';
// import store from '../../src/store'
jest.setTimeout(10000);


afterAll(() => {
  window.localStorage.setItem('Apollo-token', null)
  console.log('afterAll')
});

describe('test_unread_test_request', () => {
  console.log('des1')

// }
  // Sponsor logins
  login_helper.check_login_first_user()
  // Sponsor gets train id
  find_test_assistor_helper.get_train_id()
  // Sponsor finds assistor
  find_test_assistor_helper.onSubmit()

  // Assistor logins
  // window.localStorage.removeItem('Apollo-token')
  // store.state.is_authenticated = false
  // store.state.user_id = 0
  login_helper.check_login_second_user()
  // Assistor updates default_train_file_path, default_train_id_column, 
  // default_train_data_column
  profile_helper.onSubmit()

  
  notification_helper.update_notification()
  // console.log('rsee')
  unread_test_request_helper.unread_test_request()

  logout_helper.logout()

  //sponsor logins
  login_helper.check_login_first_user()
  // sponsor gets nofification
  notification_helper.update_notification()
  //sponsor runs unread match id
  unread_test_sponsor_match_id_helper.unread_test_sponsor_match_id()

  logout_helper.logout()
  //assistor logins
  
  login_helper.check_login_second_user()
  //assistor gets nofification
  notification_helper.update_notification()
  //sponsor runs unread match id
  unread_test_assistor_match_id_helper.unread_test_assistor_match_id()
  logout_helper.logout()

  // sponsor logins
  login_helper.check_login_first_user()
  // sponsor gets nofification
  notification_helper.update_notification()
  //sponsor runs unread situation
  unread_test_output_helper.unread_output()
  //sponsor logouts
  logout_helper.logout()
 

})
