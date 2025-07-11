import string

import allure
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime
import random
import pytest

from lib.my_requests import MyRequests

@allure.epic("Creating cases")
class TestUserRegister(BaseCase):
    email = f"learnqa{datetime.now().strftime('%m%d%Y%H%M%S')}@example.com"
    fields = [('123', 'learnqa', 'learnqa', 'learnqa', None),
              ('123', 'learnqa', 'learnqa', None, email),
              ('123', 'learnqa', None, 'learnqa', email),
              ('123', None, 'learnqa', 'learnqa', email),
              (None, 'learnqa', 'learnqa', 'learnqa', email)]

    def setup_method(self):
        base_part = 'learnqa'
        domain = 'example.com'
        random_part = datetime.now().strftime('%m%d%Y%H%M%S')
        self.email = f"{base_part}{random_part}@{domain}"
        self.incorrect_email = f"{base_part}{random_part}{domain}"

    @allure.description("Positive user creation test")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        # response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        response = MyRequests.post("/user/", data = data)
        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    @allure.description("Creating a user without email")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        # response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        response = MyRequests.post("/user/", data = data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

    @allure.description("Creating a user with incorrect email")
    def test_create_user_with_incorrect_email(self):

        data = self.prepare_registration_data(self.incorrect_email)

        # response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        response = MyRequests.post("/user/", data = data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
             "utf-8") == f"Invalid email format", f"Unexpected response content {response.content}"

    @allure.description("Creating a user with short name")
    def test_create_user_with_short_name(self):
        data = {
            'password': '123',
            'username': 'a',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        # response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        response = MyRequests.post("/user/", data = data)

        # print(response.status_code)
        # print(response.content)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too short", f"Unexpected response content {response.content}"

    @allure.description("Creating a user with long name")
    def test_create_user_with_long_name(self):
        username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=251))
        data = {
            'password': '123',
            'username': username,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        # response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        response = MyRequests.post("/user/", data = data)

        # print(response.status_code)
        # print(response.content)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The value of 'username' field is too long", f"Unexpected response content {response.content}"

    @allure.description("Creating a user without field")
    @pytest.mark.parametrize("password, username, firstname, lastname, email", fields)
    def test_create_user_without_field(self, password, username, firstname, lastname, email):

        allure.dynamic.parameter("username", username)
        allure.dynamic.parameter("password", password)
        allure.dynamic.parameter("firstName", firstname)
        allure.dynamic.parameter("lastName", lastname)
        allure.dynamic.parameter("email", email)

        data = {
            'password': password,
            'username': username,
            'firstName': firstname,
            'lastName': lastname,
            'email': email
        }

        if password is None:
            field = 'password'
        if username is None:
            field = 'username'
        if firstname is None:
            field = 'firstName'
        if lastname is None:
            field = 'lastName'
        if email is None:
            field = 'email'


        # response = requests.post('https://playground.learnqa.ru/api/user/', data=data)
        response = MyRequests.post("/user/", data = data)

        # print(response.status_code)
        # print(response.content)
        # print(field)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode(
            "utf-8") == f"The following required params are missed: {field}", f"Unexpected response content {response.content}"