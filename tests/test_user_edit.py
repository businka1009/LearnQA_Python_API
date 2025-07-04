from types import GeneratorType
from time import sleep

import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure

@allure.epic("Edit cases")
class TestUserEdit(BaseCase):

    def setup_method(self):
        with allure.step("REGISTER"):
            # REGISTER
            register_data = self.prepare_registration_data()
            # response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)
            response1 = MyRequests.post("/user/", data = register_data)


            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, 'id')

            self.email = register_data['email']
            self.first_name = register_data['firstName']
            self.password = register_data['password']
            self.user_id = self.get_json_value(response1, 'id')

            self.new_name = "Changed Name"

    @allure.description("Positive test for edit user test")
    def test_edit_just_created_user(self):

        with allure.step("LOGIN"):
            #LOGIN
            login_data = {
                'email': self.email,
                'password': self.password
            }

            # response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
            response2 = MyRequests.post("/user/login", data = login_data)


            auth_sid = self.get_cookie(response2, 'auth_sid')
            token = self.get_header(response2, 'x-csrf-token')

        with allure.step("EDIT"):
            #EDIT
            # response3 = requests.put(f'https://playground.learnqa.ru/api/user/{self.user_id}',
            #                          headers = {'x-csrf-token': token},
            #                          cookies = {'auth_sid': auth_sid},
            #                          data={'firstName': self.new_name}
            #                          )
            response3 = MyRequests.put(f"/user/{self.user_id}",
                                      headers = {'x-csrf-token': token},
                                      cookies = {'auth_sid': auth_sid},
                                      data={'firstName': self.new_name})

            Assertions.assert_code_status(response3, 200)
        with allure.step("GET"):
            #GET
            # response4 = requests.get(f'https://playground.learnqa.ru/api/user/{self.user_id}',
            #                          headers={'x-csrf-token': token},
            #                          cookies={'auth_sid': auth_sid}
            #                          )
            response4 = MyRequests.get(f"/user/{self.user_id}",
                                     headers = {'x-csrf-token': token},
                                     cookies = {'auth_sid': auth_sid})

            Assertions.assert_jason_value_by_name(
                response4,
                "firstName",
                self.new_name,
                "Wrong name of the user after edit")

    @allure.description("Editing a user without authorization in the system")
    def test_edit_unauthorized_user(self):

        with allure.step("EDIT"):
            # EDIT
            # response2 = requests.put(f'https://playground.learnqa.ru/api/user/{self.user_id}',
            #                                       data = {'firstName': self.new_name})
            response2 = MyRequests.put(f"/user/{self.user_id}",
                                     data={'firstName': self.new_name})

            Assertions.assert_code_status(response2, 400)

            assert response2.content.decode(
                "utf-8") == '{"error":"Auth token not supplied"}', f"Unexpected response content {response2.content}"

    @allure.description("Editing a user while logged in as another user")
    def test_edit_another_user(self):
        with allure.step("REGISTER second user"):
            # REGISTER
            sleep(2)
            register_data = self.prepare_registration_data()
            # response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)
            response1 = MyRequests.post("/user/", data = register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, 'id')

            email = register_data['email']
            password = register_data['password']

        with allure.step("LOGIN second user"):
            # LOGIN
            login_data = {
                'email' : email,
                'password' : password
            }

            # response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
            response2 = MyRequests.post("/user/login", data = login_data)

            auth_sid = self.get_cookie(response2, 'auth_sid')
            token = self.get_header(response2, 'x-csrf-token')

        with allure.step("EDIT first user"):
            # EDIT
            # response3 = requests.put(f'https://playground.learnqa.ru/api/user/{self.user_id}',
            #                          headers={'x-csrf-token': token},
            #                          cookies={'auth_sid': auth_sid},
            #                          data={'firstName': self.new_name}
            #                          )
            response3 = MyRequests.put(f"/user/{self.user_id}",
                                     headers = {'x-csrf-token': token},
                                     cookies = {'auth_sid': auth_sid},
                                     data={'firstName': self.new_name})


            Assertions.assert_code_status(response3, 400)
            assert response3.content.decode(
                "utf-8") == '{"error":"This user can only edit their own data."}', f"Unexpected response content {response3.content}"

    @allure.description("Editing user email to incorrect value")
    def test_edit_incorrect_email_user(self):

        with allure.step("Edit user email to incorrect value"):
            email = self.email.replace('@', '')
            # LOGIN
            login_data = {
                'email': self.email,
                'password': self.password
            }

            # response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
            response2 = MyRequests.post("/user/login", data = login_data)

            auth_sid = self.get_cookie(response2, 'auth_sid')
            token = self.get_header(response2, 'x-csrf-token')

        with allure.step("EDIT user"):
            # EDIT
            # response3 = requests.put(f'https://playground.learnqa.ru/api/user/{self.user_id}',
            #                          headers={'x-csrf-token': token},
            #                          cookies={'auth_sid': auth_sid},
            #                          data={'email': email}
            #                          )
            response3 = MyRequests.put(f"/user/{self.user_id}",
                                     headers = {'x-csrf-token': token},
                                     cookies = {'auth_sid': auth_sid},
                                     data={'email': email})


            Assertions.assert_code_status(response3, 400)
            assert response3.content.decode(
                "utf-8") == '{"error":"Invalid email format"}', f"Unexpected response content {response3.content}"

    @allure.description("Edit username to be too short")
    def test_edit_shot_firstname_user(self):
        # LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }

        # response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)
        response2 = MyRequests.post("/user/login", data = login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        # response3 = requests.put(f'https://playground.learnqa.ru/api/user/{self.user_id}',
        #                          headers={'x-csrf-token': token},
        #                          cookies={'auth_sid': auth_sid},
        #                          data={'firstName': 'a'}
        #                          )
        response3 = MyRequests.put(f"/user/{self.user_id}",
                                 headers = {'x-csrf-token': token},
                                 cookies = {'auth_sid': auth_sid},
                                 data={'firstName': 'a'})

        Assertions.assert_code_status(response3, 400)

        assert response3.content.decode(
            "utf-8") == '{"error":"The value for field `firstName` is too short"}', f"Unexpected response content {response3.content}"














