class TestEx10:
    def test_check_phrase(self):
       phrase = input("Введите фразу: ")
       assert len(phrase) < 15, f"Фраза '{phrase}' больше 15 символов"

