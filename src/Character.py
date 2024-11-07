import json
from dicts import attributes_checks


class Character:
    default_attack_bonus = 3
    main_attribute = "cha"
    stats: dict = {}
    skills: dict = {}
    name: str = ""
    proficiency: int = 0

    def get_stat_bonus_value(self, attr: str) -> int:
        return (
            ((self.stats[attr]["value"] // 2) - 5) if attr in self.stats.keys() else 0
        )

    def get_skill_overall_bonus(self, attr_en: str) -> int:
        value: int = 0
        if attr_en in self.skills.keys():
            skill: dict = self.skills[attr_en]
            value = skill["bonus"] + self.get_stat_bonus_value(skill["stat"])

        if attr_en in self.stats.keys():
            value = self.get_stat_bonus_value(attr_en)
        return value

    def get_attack_roll(self, roll: int):
        label_en = "attack check"
        value: int = (
            self.get_stat_bonus_value(self.main_attribute) + self.default_attack_bonus
        )

        return {
            "character_name": self.name,
            "label_en": label_en,
            "label": None,
            "value": roll + value,
            "roll": roll,
            "bonus": value,
            "main_text": attributes_checks[label_en],
        }

    def get_stat_roll(self, roll: int, label_en: str) -> dict:
        value: int = 0
        label: str = ""

        if label_en in self.skills.keys():
            skill: dict = self.skills[label_en]
            label: str = skill["labelRu"]
            # attr_bonus: int = self.get_stat_bonus_value(skill["stat"])
            # value = skill["bonus"] + attr_bonus
            value = self.get_skill_overall_bonus(label_en)

        elif label_en in self.stats.keys():
            stat: dict = self.stats[label_en]
            value = self.get_skill_overall_bonus(label_en)
            label = stat["labelRu"]

        return {
            "character_name": self.name,
            "label_en": label_en,
            "label": label,
            "value": roll + value,
            "roll": roll,
            "bonus": value,
            "main_text": attributes_checks[label_en],
        }

    def load_data_from_json(self, data):
        try:
            src_data = json.load(data)
            char_list = json.loads(src_data["data"])

            self.name = char_list["name"]["value"]
            self.proficiency = int(char_list["proficiency"])

            for skill in char_list["skills"]:
                self.skills[skill] = {
                    "stat": char_list["skills"][skill].get("baseStat", 0),
                    "labelEn": char_list["skills"][skill]["name"],
                    "labelRu": char_list["skills"][skill]["label"],
                    "bonus": (int(char_list["skills"][skill].get("isProf", 0)) * 3),
                }

            for stat in char_list["stats"]:
                self.stats[stat] = {
                    "name": char_list["stats"][stat]["name"],
                    "labelRu": char_list["stats"][stat]["label"],
                    "value": (int(char_list["stats"][stat].get("score", 0))),
                }
        except Exception as e:
            print(e)
