import requests
import time
import json

key1 = "token"
key2 = "seconds"
key3 = "status"
key4 = "result"

response1 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job")
json_text1 = response1.json()
print(json_text1)
response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={key1: json_text1[key1]})
json_text2 = response2.json()
print(json_text2)
if json_text2[key3] == "Job is NOT ready":
    time.sleep(json_text1[key2])
    response3 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={key1: json_text1[key1]})
    json_text3 = response3.json()
    print(json_text3)
    if json_text3[key3] == "Job is ready":
        if key4 in json_text3:
            print(json_text3[key4])
elif json_text2[key3] == "Job is ready":
    if key4 in json_text2:
        print(json_text2[key4])







# print(response1.text)
# response2 = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params = {"token":"ANyoDO1oTNxACMx0iNw0SNyAjM"})
# print(response2.text)