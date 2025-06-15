import requests
import pytest
import json

class TestEx13:
    user_agents = [("Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
                    "Mobile",
                    "No",
                    "Android"),
                   ("Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1",
                    "Mobile",
                    "Chrome",
                    "iOS"),
                   ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                    "Googlebot",
                    "Unknown",
                    "Unknown"),
                   ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0",
                    "Web",
                    "Chrome",
                    "No"),
                   ("Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
                    "Mobile",
                    "No",
                    "iPhone")]



    @pytest.mark.parametrize("user_agent, platform, browser, device", user_agents)
    def test_check_user_agent(self, user_agent, platform, browser, device):
      platform_key = 'platform'
      browser_key = 'browser'
      device_key = 'device'
      url = "https://playground.learnqa.ru/ajax/api/user_agent_check"
      response = requests.get(url, headers={"User-Agent": user_agent})
      json_text = response.json()
      print(json_text)
      print(platform)
      print(browser)
      print(device)
      # assert 2 == 2
      if platform_key in json_text:
        assert json_text[platform_key] == platform, f"Значение ключа {platform_key} - {json_text[platform_key]} не совпадает с ожидаемым значением - {platform}"
      else:
          print(f"Ключ {platform_key} отсутствует в JSON")
      if browser_key in json_text:
        assert json_text[browser_key] == browser, f"Значение ключа {browser_key} - {json_text[browser_key]} не совпадает с ожидаемым значением - {browser}"
      else:
          print(f"Ключ {browser_key} отсутствует в JSON")
      if device_key in json_text:
          assert json_text[device_key] == device, f"Значение ключа {device_key} - {json_text[device_key]} не совпадает с ожидаемым значением - {device}"
      else:
          print(f"Ключ {device_key} отсутствует в JSON")
