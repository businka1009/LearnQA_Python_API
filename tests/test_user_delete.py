from time import sleep

import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure

from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):
    @allure.description("Deleting user with id=2")
    def test_delete_user_id2(self):
        with allure.step("LOGIN"):
            # LOGIN
            login_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }

            # response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
            response1 = MyRequests.post('/user/login', data=login_data)

            auth_sid = self.get_cookie(response1, 'auth_sid')
            token = self.get_header(response1, 'x-csrf-token')

        with allure.step("DELETE"):
            # DELETE
            # response2 = requests.delete(f'https://playground.learnqa.ru/api/user/{auth_sid}',
            #                          headers={'x-csrf-token': token},
            #                          cookies={'auth_sid': auth_sid}
            #                          )

            response2 = MyRequests.delete(f'/user/{auth_sid}',
                                          headers={'x-csrf-token': token},
                                          cookies={'auth_sid': auth_sid}
                                          )

            Assertions.assert_code_status(response2, 404)
            assert response2.content.decode(
                "utf-8") == "int(2)\nThis is 404 error!\n<a href='/'>Home</a>", f"Unexpected response content {response2.content}"

    @allure.description("Normal user deletion")
    def test_delete_just_user(self):
        with allure.step("REGISTER"):
            # REGISTER
            register_data = self.prepare_registration_data()
            # response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, 'id')

            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, 'id')

        with allure.step("LOGIN"):
            # LOGIN
            login_data = {
                'email': email,
                'password': password
            }

            # response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
            response2 = MyRequests.post('/user/login', data=login_data)

            auth_sid = self.get_cookie(response2, 'auth_sid')
            token = self.get_header(response2, 'x-csrf-token')

        with allure.step("DELETE"):
            # DELETE
            # response3 = requests.delete(f'https://playground.learnqa.ru/api/user/{user_id}',
            #                          headers={'x-csrf-token': token},
            #                          cookies={'auth_sid': auth_sid}
            #                          )

            response3 = MyRequests.delete(f'/user/{user_id}',
                                          headers={'x-csrf-token': token},
                                          cookies={'auth_sid': auth_sid}
                                          )

            Assertions.assert_code_status(response3, 200)

        with allure.step("GET"):
            # GET
            # response4 = requests.get(f'https://playground.learnqa.ru/api/user/{user_id}',
            #                          headers={'x-csrf-token': token},
            #                          cookies={'auth_sid': auth_sid}
            #                          )
            response4 = MyRequests.get(f'/user/{user_id}',
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid}
                                       )
            assert response4.content.decode(
                "utf-8") == "User not found", f"Unexpected response content {response4.content}"

    @allure.description("Delete another user")
    def test_delete_another_user(self):
        with allure.step("REGISTER first user"):
            # REGISTER1
            register_data = self.prepare_registration_data()
            # response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, 'id')

            user_id = self.get_json_value(response1, 'id')

        with allure.step("REGISTER second user"):
            # REGISTER2
            sleep(2)
            register_data2 = self.prepare_registration_data()
            # response2 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data2)
            response2 = MyRequests.post('/user/', data=register_data2)

            Assertions.assert_code_status(response2, 200)
            Assertions.assert_json_has_key(response2, 'id')

            email2 = register_data2['email']
            password2 = register_data2['password']

        with allure.step("LOGIN second user"):
            # LOGIN
            login_data = {
                'email' : email2,
                'password' : password2
            }

            # response3 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
            response3 = MyRequests.post('/user/login', data=login_data)

            auth_sid = self.get_cookie(response3, 'auth_sid')
            token = self.get_header(response3, 'x-csrf-token')

        with allure.step("DELETE first user"):
            # DELETE
            # response4 = requests.delete(f'https://playground.learnqa.ru/api/user/{user_id}',
            #                             headers={'x-csrf-token': token},
            #                             cookies={'auth_sid': auth_sid}
            #                             )

            response4 = MyRequests.delete(f'/user/{user_id}',
                                          headers={'x-csrf-token': token},
                                          cookies={'auth_sid': auth_sid}
                                          )

            Assertions.assert_code_status(response4, 400)
            assert response4.content.decode(
                "utf-8") == '{"error":"This user can only delete their own account."}', f"Unexpected response content {response4.content}"



