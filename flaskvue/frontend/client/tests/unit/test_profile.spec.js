import { login_helper } from './helper_folder/Apollo_login_helper'
import { profile_helper } from './helper_folder/Apollo_profile_helper'
jest.setTimeout(10000);

afterAll(() => {
  window.localStorage.setItem('Apollo-token', null)
  console.log('afterAll')
});

describe('test_profile', () => {
  login_helper.check_login_second_user
  profile_helper.onSubmit
})
