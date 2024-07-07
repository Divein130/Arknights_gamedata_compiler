import json
import os
import shutil
import re


def parse_story_review_table(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        return json_data
    return None


def get_context_from_story_txt(txt_path):
    story_directory = os.path.join(os.getcwd(), os.path.normpath(gamedata_directory), 'story')
    txt_directory = os.path.join(story_directory, os.path.normpath(txt_path) + '.txt')
    with open(txt_directory, 'r', encoding='utf-8') as f:
        return f.read()
    return None


def parse_story_json(json_data):
    activity_codes = json_data.keys()
    story_data = {}
    for activity_code in activity_codes:
        activity_info = json_data[activity_code]
        name = activity_info['name']
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


def safe_concat_level_name(*args):
    return '_'.join([arg if arg is not None else '' for arg in args])


def output_groupby_level(story_data):
    output_directory = 'story_context'
    output_directory = os.path.join(os.getcwd(), output_directory)
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
        print(f"目录已存在，已删除：{output_directory}")
    os.makedirs(output_directory, exist_ok=True)
    illegal_chars = r'[<>:"/\\|?*]'
    for story_id in story_data.keys():
        story = story_data[story_id]
        story_name = story['name']
        for level in story['level_list']:
            if level.get('story_code') is None:
                continue
            level_name = safe_concat_level_name(story_name, level.get('story_name'), level.get('story_code'),
                                                level.get('avg_tag'))
            level_context = get_context_from_story_txt(level['story_txt_path'])
            file_name = level_name + '.txt'
            clean_file_name = re.sub(illegal_chars, '-', file_name)

            file_path = os.path.join(output_directory, clean_file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(normalize_dialogue(level_context))


def output_groupby_story(story_data):
    output_directory = 'story_context_story'
    output_directory = os.path.join(os.getcwd(), output_directory)
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
        print(f"目录已存在，已删除：{output_directory}")
    os.makedirs(output_directory, exist_ok=True)
    illegal_chars = r'[<>:"/\\|?*]'
    for story_id in story_data.keys():
        story = story_data[story_id]
        story_name = story['name']
        story_context = []
        for level in story['level_list']:
            level_name = safe_concat_level_name('<', level.get('story_code'), level.get('story_name'),
                                                level.get('avg_tag'), '>')

            level_context = get_context_from_story_txt(level['story_txt_path'])
            level_context = normalize_dialogue(level_context)
            story_context.append(level_name)
            story_context.append(level_context)
        file_name = story_name + '.txt'
        clean_file_name = re.sub(illegal_chars, '-', file_name)

        file_path = os.path.join(output_directory, clean_file_name)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(os.linesep.join(story_context))

def normalize_dialogue(input_text):
    # 定义正则表达式模式来匹配对话内容
    name_pattern = re.compile(r'\[name="([^"]+)"\]')
    charslot_pattern = re.compile(r'\[charslot\(.*?\)\]')
    dialogue_pattern = re.compile(r'\[name="([^"]+)"\](.*)')

    # 存储归一化的对话
    normalized_lines = []

    # 按行处理输入文本
    lines = input_text.splitlines()
    for line in lines:
        # 跳过charslot行
        if charslot_pattern.match(line):
            continue

        # 处理对话行
        match = dialogue_pattern.match(line)
        if match:
            name = match.group(1)
            dialogue = match.group(2).strip()
            normalized_lines.append(f'[{name}]: {dialogue}')
        else:
            # 处理非对话行（如stopmusic, delay等）
            continue

    return os.linesep.join(normalized_lines)


# 如果需要指定gamedata，请修改以下路径
gamedata_directory = './gamedata'
story_review_table_directory = os.path.join(gamedata_directory, 'excel', 'story_review_table.json')

json_data = parse_story_review_table(story_review_table_directory)
if json_data is None:
    print(f"[ERROR] Can't find any story review table {story_review_table_directory}")
    exit(1)
story_data = parse_story_json(json_data)

# output_groupby_level(story_data)
output_groupby_story(story_data)

# print(story_data)
