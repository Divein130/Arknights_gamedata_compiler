import json
import os.path

directory = '../ArknightsGamedataPure/levels/enemydata/enemy_database.json'

with open(os.path.normcase(os.path.join(os.getcwd(), directory)), 'r', encoding='utf-8') as f:
    data = json.load(f)
    for enemy in data['enemies']:
        for data in enemy['value']:
            if str(data.get('enemyData').get('name').get('m_value')).__contains__('萨尔古斯'):
                print('萨尔古斯抗性:' + str(data.get('enemyData').get('attributes').get('fearedImmune').get('m_value')))
            if str(data.get('enemyData').get('name').get('m_value')).__contains__('大地之鞭'):
                print('大地之鞭抗性:' + str(data.get('enemyData').get('attributes').get('fearedImmune').get('m_value')))
            if data.get('enemyData').get('attributes').get('fearedImmune').get('m_value'):
                print(data.get('enemyData').get('name').get('m_value'))
