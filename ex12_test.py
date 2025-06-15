import requests

class TestEx12:
    def test_check_headers(self):
      url = "https://playground.learnqa.ru/api/homework_header"
      response = requests.get(url)
      header = dict(response.headers)
      print(header)
      assert "Date" in header, f"'Date' отсутствует в {header}"
      assert "Content-Type" in header, f"'Content-Type' отсутствует в {header}"
      assert "Content-Length" in header, f"'Content-Length' отсутствует в {header}"
      assert "Connection" in header, f"'Connection' отсутствует в {header}"
      assert "Keep-Alive" in header, f"'Keep-Alive' отсутствует в {header}"
      assert "Server" in header, f"'Server' отсутствует в {header}"
      assert "x-secret-homework-header" in header, f"'Server' отсутствует в {header}"
      assert "Cache-Control" in header, f"'Cache-Control' отсутствует в {header}"
      assert "Expires" in header, f"'Expires' отсутствует в {header}"





