import os
from rich import print
import json
from InquirerPy import prompt
import fullscreen.fullscreen as fs
import pandas as pd

config = {}
init = False

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    init = True
except json.JSONDecodeError:
    print("Error: 설정 파일을 불러오는 중 문제가 발생했습니다. 설정 파일을 삭제하고 다시 실행해주세요.")

def select_region():
    sr_config = {}
    cache_file = 'cache.pkl'

    df = pd.DataFrame()

    if os.path.exists(cache_file):
        # 캐시된 파일이 존재하면, 캐시된 파일을 읽습니다.
        df = pd.read_pickle(cache_file)
    else:
        # 캐시된 파일이 존재하지 않으면, 원본 파일을 읽고 그 결과를 캐시 파일에 저장합니다.
        df = pd.read_excel('st.xlsx')
        df.to_pickle(cache_file)

    question_1_res = prompt({
        'type': 'list',
        'name': 'location_1',
        'message': '도시를 선택하세요.',
        'choices': sorted(set(df['1단계'].dropna().astype(str).to_list()))
    })

    df = df[df['1단계'] == question_1_res['location_1']]
    
    question_2_res = prompt({
        'type': 'list',
        'name': 'location_2',
        'message': '지역구를 선택하세요.',
        'choices': sorted(set(df['2단계'].dropna().astype(str).to_list()))
    })

    df = df[df['2단계'] == question_2_res['location_2']]

    question_3_res = prompt({
        'type': 'list',
        'name': 'location_3',
        'message': '동네를 선택하세요.',
        'choices': sorted(set(df['3단계'].dropna().astype(str).to_list()))
    })

    df = df[df['3단계'] == question_3_res['location_3']]
    selected_location = f"{question_1_res['location_1']} {question_2_res['location_2']} {question_3_res['location_3']}"

    confirm_res = prompt({
        'type': 'confirm',
        'name': 'confirm',
        'message': f'{selected_location}이 맞습니까?'
    })

    if confirm_res['confirm'] == False:
        return select_region()

    sr_config['location'] = (df['격자 X'].to_list()[0], df['격자 Y'].to_list()[0])

    return sr_config


# 설정 파일이 없는 경우, 사용자에게 설정을 입력받습니다.

if init == True:
    cache_file = 'cache.pkl'

    df = pd.DataFrame()

    if os.path.exists(cache_file):
        # 캐시된 파일이 존재하면, 캐시된 파일을 읽습니다.
        df = pd.read_pickle(cache_file)
    else:
        # 캐시된 파일이 존재하지 않으면, 원본 파일을 읽고 그 결과를 캐시 파일에 저장합니다.
        df = pd.read_excel('st.xlsx')
        df.to_pickle(cache_file)

    print("WeatherPy 를 처음 실행하셨군요! 기본 설정을 진행합니다.")

    with open('config.json', 'w') as f:
        json.dump(select_region(), f)
