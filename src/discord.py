from settings import WEBHOOK_URL, CHAR_PHOTO_URL
import requests
from dicts import attributes_checks

name: str = ...

# embed = {
#     "title": "Проверка Интеллекта — 8",
#     "author": {
#         "name": f"{name}",
#     },
#     "color": 16711680,  # Цвет эмбеда (красный)
#     "thumbnail": {
#         "url": "https://images-ext-1.discordapp.net/external/_hUCkxTfRLMbLVIAjl6hEufw60NpwBaO9ILo1q_GAGQ/%3Fmod%3D1698785897663/https/lss-s3-files.s3.eu-north-1.amazonaws.com/avatar/653d66fdb3290e0cd80f34f9.jpeg?format=webp"  # Ссылка на изображение
#     },
#     "fields": [
#         {"name": "", "value": "(9) - 1", "inline": True},
#     ],
#     "footer": {  # Добавляем футер
#         "text": "(1к20) - 1",  # Текст футера
#     },
# }

# data = {"username": f"{name.split()[0]}", "embeds": [embed]}

# result = requests.post(WEBHOOK_URL, json=data)


class Discord:
    url: str = ""
    photo_url: str = ""
    embed: dict = {}
    data: dict = {}

    def __init__(self, url, photo_url):
        self.url = url
        self.photo_url = photo_url

    def create_embed(self, roll_dict: dict, dice: str):
        """
        roll_dict:  "character_name": self.name, \\
                    "label_en": label_en, \\
                    "label": label, \\
                    "value": roll + value, \\
                    "roll": roll, \\
                    "bonus": value, \\
                    "main_text": attributes_checks['label_en'] 
        """
        footer_text = f"({dice}) {f"- {abs(roll_dict['bonus'])}" if roll_dict['bonus'] < 0 else f"+ {abs(roll_dict['bonus'])}"}"
        main_text = f"({roll_dict["roll"]}) {f"- {abs(roll_dict['bonus'])}" if roll_dict['bonus'] < 0 else f"+ {abs(roll_dict['bonus'])}"}"

        check_text = roll_dict["main_text"]

        title_text = ""
        if roll_dict["roll"] == 20:
            title_text = f"🔥 {check_text} — {roll_dict['value']} 🔥"
        elif roll_dict["roll"] == 1:
            title_text = f"🩸 {check_text} — {roll_dict['value']} 🩸"
        else:
            title_text = f"{check_text} — {roll_dict['value']}"

        self.embed = {
            "title": title_text,
            "author": {
                "name": f"{roll_dict['character_name']}",
            },
            "color": 0x03A9F4,  # Цвет эмбеда (красный)
            "thumbnail": {"url": f"{CHAR_PHOTO_URL}"},
            "fields": [
                {
                    "name": "",
                    "value": main_text,
                    "inline": True,
                },
            ],
            "footer": {  # Добавляем футер
                "text": footer_text,  # Текст футера
            },
        }
        self.data = {
            "username": f"{roll_dict['character_name'].split()[0]}",
            "embeds": [self.embed],
        }

    def send_embed(self):
        try:
            requests.post(self.url, json=self.data)
        except Exception as e:
            print(e)
