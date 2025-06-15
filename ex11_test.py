import requests

class TestEx11:
    def test_check_cookies(self):
      url = "https://playground.learnqa.ru/api/homework_cookie"
      response = requests.get(url)
      cookie = dict(response.cookies)
      print(cookie)
      cookie_value = cookie.get("HomeWork")
      assert "HomeWork" in cookie, "Имя cookie не совпадает с тем, что выведено на экране"
      assert cookie_value == "hw_value", "Значение cookie не совпадает с тем, что выведено на экране"
