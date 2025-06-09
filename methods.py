import requests

response1 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type")
print(f'RESPONSE1: {response1.text}')

response2 = requests.patch("https://playground.learnqa.ru/ajax/api/compare_query_type", data={'method':'PATCH'})
print(f'RESPONSE2: {response2.text}')

response3 = requests.get("https://playground.learnqa.ru/ajax/api/compare_query_type", params={'method': 'GET'})
print(f'RESPONSE3: {response3.text}')

methods = ['GET', 'POST', 'PUT','DELETE']
for method in methods:
    for method2 in methods:
        if method == 'GET':
            response = requests.request(method=method, url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                                        params={'method': method2})
            print(f'RESPONSE_{method}, method_{method2}: {response.text}')
        else:
            response = requests.request(method=method, url="https://playground.learnqa.ru/ajax/api/compare_query_type",
                                        data={'method': method2})
            print(f'RESPONSE_{method}, method_{method2}: {response.text}')





