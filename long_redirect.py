import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect", allow_redirects=True)
count_redirect = len(response.history)

print(count_redirect)
print(response.url)