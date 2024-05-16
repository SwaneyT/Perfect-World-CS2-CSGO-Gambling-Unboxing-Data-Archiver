import ast
import json

with open("china_translation_organised.txt","r",encoding="utf-8") as chinese_english_file:
    chinese_english_contents = chinese_english_file.read()

chinese_english_json = ast.literal_eval(chinese_english_contents)


def translateChineseToEnglish(chinese):
    try:
        return chinese_english_json[chinese]
    except Exception as e:
        return None


# print(translateChineseToEnglish('弯刀（★ StatTrak™） | 自动化 (久经沙场)'))