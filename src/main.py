# import json
import os
from Character import Character
from settings import LSS_CHARACTER_JSON_LIST_PATH, WEBHOOK_URL, CHAR_PHOTO_URL
from dicts import attributes_menu, attributes_menu_en
from discord import Discord
import random

discord_service = Discord(WEBHOOK_URL, CHAR_PHOTO_URL)


def get_random_value(min: int, max: int) -> int:
    return random.randint(min, max)


def handleAction(character: Character, action: int):
    if action == 0:
        exit(0)

    if 1 <= action <= 24:
        dice: str = "1к20"
        attr: str = attributes_menu_en[action]
        print(f"Выбранное действие проверка {attributes_menu[action]}")
        print(
            f"> Выберите желаемое минимальное значение не превышающее {20 + character.get_skill_overall_bonus(attr)}"
        )
        desired_value = int(input())

        roll_value = 2
        while character.get_stat_roll(roll_value, attr)["value"] < desired_value:
            roll_value = get_random_value(1, 20)
            # print(f"trying with {roll_value}")

        res = character.get_stat_roll(roll_value, attr)
        print(res)

        discord_service.create_embed(res, "1к20")
        discord_service.send_embed()

    if action == 25:
        dice = "1к20"
        print(f"Выбранное действие {attributes_menu[action]}")
        print(
            f"> Выберите желаемое минимальное значение не превышающее {23 + character.get_stat_bonus_value(character.main_attribute)}"
        )
        desired_value = int(input())

        roll_value = 2
        while character.get_attack_roll(roll_value)["value"] < desired_value:
            print(f"trying with {roll_value}", character.get_attack_roll(roll_value))
            roll_value = get_random_value(desired_value - int(dice.split("к")[1]), 20)

        res = character.get_attack_roll(roll_value)
        discord_service.create_embed(res, "1к20")
        discord_service.send_embed()

    if action == 26:
        print("> Введите кубик (пример 1к20)")
        dice = input()
        amount, max_number = (
            map(int, dice.split("к")) if "к" in dice else 1,
            20,
        )

        print(
            f"> Выберите желаемое минимальное значение не превышающее {amount * max_number}"
        )

        desired_value = int(input())
        if 1 <= desired_value <= amount * max_number:
            ...

            # create_embed(dice, roll_value, result_value)
            # if (should_send_embed()):
            # send_embed()


def printMenu() -> None:
    os.system("cls")
    print("\n" + "=" * 120)
    print("   Меню проверки характеристик".center(120))
    print("=" * 120)

    max_key_length = len(str(max(attributes_menu.keys())))
    max_value_length = max(len(value) for value in attributes_menu.values())
    format_string = f"%{max_key_length}d. %-{max_value_length}s"

    options_per_row = 3
    keys = list(attributes_menu.keys())
    for i in range(0, len(keys), options_per_row):
        row_keys = keys[i : i + options_per_row]
        row_strings = []
        for key in row_keys:
            row_strings.append(format_string % (key, attributes_menu[key]))
        print(" | ".join(row_strings).center(120))

    print("0. Выход\n".center(120))


def main():
    char = Character()

    with open(LSS_CHARACTER_JSON_LIST_PATH, "r", encoding="UTF-8") as f:
        char.load_data_from_json(f)

    # while True:
    printMenu()
    action = int(input())
    handleAction(char, action)


def test():
    char = Character()

    with open(LSS_CHARACTER_JSON_LIST_PATH, "r", encoding="UTF-8") as f:
        char.load_data_from_json(f)

    for name, stat in char.stats.items():
        print(name, stat)
    for name, skill in char.skills.items():
        print(name, skill)


main()
# test()

# except Exception as e:
#     print(e.with_traceback)


# # print(char.stats)
# print(f"Проверка Ловкости {char.get_stat_roll(10, 'dex')} {char.get_stat_roll(10, 'dex')['value'] == 13}")
# print(f"Проверка Магии {char.get_stat_roll(10, 'arcana')} {char.get_stat_roll(10, 'arcana')['value'] == 15}")
# print(f"Проверка persuasion {char.get_stat_roll(10, 'persuasion')} {char.get_stat_roll(10, 'persuasion')['value'] == 16}")


# try:
#      result.raise_for_status()
# except requests.exceptions.HTTPError as err:
#     print(err)
# else:
#     print("Сообщение успешно отправлено.")
