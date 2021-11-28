  

import { mount } from '@vue/test-utils';
// import Counter from './counter'
import Navbar from '../../src/components/Navbar.vue'
import db from '../../src/db';
import axios from 'axios'
// jest.mock("axios")

window.require = require;

// const Navbar = require('../../components/Navbar.vue');

// 现在挂载组件，你便得到了这个包裹器
// const wrapper = mount(Counter)
// const wrapper =  mount(Navbar)

// 你可以通过 `wrapper.vm` 访问实际的 Vue 实例
// const vm = wrapper.vm

// 在控制台将其记录下来即可深度审阅包裹器
// 我们对 Vue Test Utils 的探索也由此开始
// console.log(wrapper)
// jest.mock("axios", () => ({
//     get: () => Promise.resolve({ data: [{ val: 1 }] })
//   }));


describe('Navbar', () => {
    // 现在挂载组件，你便得到了这个包裹器
    // const wrapper = mount(Navbar)
    
    const wrapper = mount(Navbar, {
        mocks: {
           $toasted: {
               success: () => {},
           }
        },
        stubs: ['router-link','router-view']
      });
  
    // 也便于检查已存在的元素
    
    
    const users = [{ id: 1, name: "testa" }, { id: 2, name: "testb" }];
    const test_example = {
        check_dict: { "e7bc07bc-568b-4917-b774-9961729da1c2": "1"}
    }

    
    it('function async', () => {
        axios.get = jest.fn().mockReturnValue(users);
        // let mockFn = jest.fn().mockReturnValue('default');
        axios.post = jest.fn().mockReturnValue(users);
        db.get = jest.fn().mockReturnValue(users);

        wrapper.vm.sharedState.user_id = 2
        

        // wrapper.vm.$nextTick(() => {
        //     expect(wrapper.vm.test_response).toEqual(users);
        //   });
        // const result = wrapper.vm.unread_request(test_example);
        // expect(wrapper.vm.test_response.length).toBe(1);
        const result = axios.get('/send_situation/')
        expect(result).toEqual(users);
        const result1 = db.get()
        expect(result1).toEqual(users);
        const result2 = axios.post('/send_situation/')
        expect(result2).toEqual(users);
        expect(wrapper.vm.unread_request(test_example)).toBe('done');
      })

      



      

    


  })