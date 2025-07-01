import pytest
import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
import allure


@allure.epic("Authorization cases")
class TestUserAuth(BaseCase):

    exclude_params = [
        ("no_cookies"),
        ("no_token")
    ]

    def setup_method(self):
        data = {
            'email' : 'vinkotov@example.com',
            'password' : '1234'
        }

        # response1 = requests.post('https://playground.learnqa.ru/api/user/login', data=data)
        response1 = MyRequests.post("/user/login", data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth_method = self.get_json_value(response1, "user_id")

    @allure.description("This test successfully authorize user by email and password")
    def test_auth_user(self):

        # response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
        #                          headers={'x-csrf-token': self.token},
        #                          cookies={'auth_sid': self.auth_sid}
        #                          )
        with allure.step("Check user by token and id"):
            response2 = MyRequests.get("/user/auth", headers={'x-csrf-token': self.token}, cookies={'auth_sid': self.auth_sid})

        with allure.step("Assert that user id is valid"):
            Assertions.assert_jason_value_by_name(
                response2,
                "user_id",
                self.user_id_from_auth_method,
                "User id from method is not equal to user id from check method"
            )


    @allure.description("This test chack authorization status w/o sending auth cookie or token")
    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth_check(self, condition):
        with allure.step("Check user by token and id"):
            if condition == 'no_cookies':
                # response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                #                          headers={'x-csrf-token': self.token}
                #                          )
                response2 = MyRequests.get("/user/auth", headers={'x-csrf-token': self.token})
            else:
                # response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                #                          cookies={'auth_sid': self.auth_sid}
                #                          )
                response2 = MyRequests.get("/user/auth", cookies={'auth_sid': self.auth_sid})
        with allure.step("Assert that user id is valid"):
            Assertions.assert_jason_value_by_name(
                response2,
                "user_id",
                0,

                f"User is authorized with condition {condition}"
                )





