from types import GeneratorType

import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserEdit(BaseCase):

    def setup_method(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        self.email = register_data['email']
        self.first_name = register_data['firstName']
        self.password = register_data['password']
        self.user_id = self.get_json_value(response1, 'id')

        self.new_name = "Changed Name"

    def test_edit_just_created_user(self):

        #LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)


        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        #EDIT
        response3 = requests.put(f'https://playground.learnqa.ru/api/user/{self.user_id}',
                                 headers = {'x-csrf-token': token},
                                 cookies = {'auth_sid': auth_sid},
                                 data={'firstName': self.new_name}
                                 )

        Assertions.assert_code_status(response3, 200)

        #GET
        response4 = requests.get(f'https://playground.learnqa.ru/api/user/{self.user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid}
                                 )

        Assertions.assert_jason_value_by_name(
            response4,
            "firstName",
            self.new_name,
            "Wrong name of the user after edit")

    def test_edit_unauthorized_user(self):

        # EDIT
        response2 = requests.put(f'https://playground.learnqa.ru/api/user/{self.user_id}',
                                              data = {'firstName': self.new_name})

        Assertions.assert_code_status(response2, 400)

        assert response2.content.decode(
            "utf-8") == '{"error":"Auth token not supplied"}', f"Unexpected response content {response2.content}"


    def test_edit_another_user(self):
        # LOGIN
        login_data = {
            'email' : 'vinkotov@example.com',
            'password' : '1234'
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        response3 = requests.put(f'https://playground.learnqa.ru/api/user/{self.user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid},
                                 data={'firstName': self.new_name}
                                 )

        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            "utf-8") == '{"error":"Please, do not edit test users with ID 1, 2, 3, 4 or 5."}', \
            f"Unexpected response content {response3.content}"


    def test_edit_incorrect_email_user(self):

        email = self.email.replace('@', '')
        # LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        response3 = requests.put(f'https://playground.learnqa.ru/api/user/{self.user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid},
                                 data={'email': email}
                                 )


        Assertions.assert_code_status(response3, 400)
        assert response3.content.decode(
            "utf-8") == '{"error":"Invalid email format"}', f"Unexpected response content {response3.content}"

    def test_edit_shot_firstname_user(self):
        # LOGIN
        login_data = {
            'email': self.email,
            'password': self.password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, 'auth_sid')
        token = self.get_header(response2, 'x-csrf-token')

        # EDIT
        response3 = requests.put(f'https://playground.learnqa.ru/api/user/{self.user_id}',
                                 headers={'x-csrf-token': token},
                                 cookies={'auth_sid': auth_sid},
                                 data={'firstName': 'a'}
                                 )

        Assertions.assert_code_status(response3, 400)

        assert response3.content.decode(
            "utf-8") == '{"error":"The value for field `firstName` is too short"}', f"Unexpected response content {response3.content}"














