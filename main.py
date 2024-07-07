import json
import os

def parse_story_review_table(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        return json_data
    return None

def get_context_from_story_txt(txt_path):
    story_directory = os.path.join(gamedata_directory, 'story')
    txt_directory = os.path.join(story_directory, txt_path)
    with open(txt_directory, 'r', encoding='utf-8') as f:
        return f.read()
    return None


def parse_story_json(json_data):
    activity_codes = json_data.keys()
    story_data = {}
    for activity_code in activity_codes:
        activity_info = json_data[activity_code]
        name = activity_info['name']
        # print(f"Name: {name}")
        if activity_code not in story_data:
            story_data[activity_code] = {}
            story_data[activity_code]['activity_code'] = activity_code
            story_data[activity_code]['name'] = name
            story_data[activity_code]['level_list'] = []
        for level in activity_info['infoUnlockDatas']:
            story_txt_path = level.get('storyTxt')
            story_name = level.get('storyName')
            story_info_path = level.get('storyInfo')
            story_code = level.get('storyCode')
            avg_tag = level.get('avgTag')
            story_data[activity_code]['level_list'].append({
                'story_txt_path': story_txt_path,
                'story_name': story_name,
                'story_info_path': story_info_path,
                'story_code': story_code,
                'avg_tag': avg_tag,
            })
    return story_data
# 使用示例
gamedata_directory = './gamedata'
story_review_table_directory = os.path.join(gamedata_directory, 'excel', 'story_review_table.json')

json_data = parse_story_review_table(story_review_table_directory)
if json_data is None:
    print(f"[ERROR] Can't find any story review table {story_review_table_directory}")
    exit(1)
story_data = parse_story_json(json_data)

print(story_data)

