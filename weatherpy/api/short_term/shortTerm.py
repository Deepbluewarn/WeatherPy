import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from tools.translator import api_err_translator
from tools.config import getUserConfig

load_dotenv()

# 기상청 단기 예보 조회 API 호출
# 오늘 날짜를 기준으로 단기 예보 정보를 가져옵니다.

def getShortTermWeatherInfo(date):
    config = getUserConfig()
    url = os.environ.get('API_ST_BASE_URL') + '/getVilageFcst'
    params = {
        'serviceKey' : os.environ.get('SERVICE_KEY'), 
        'pageNo' : '1', 
        'numOfRows' : '1000', 
        'dataType' : 'JSON', 
        'base_date' : date, 
        'base_time' : '0200', 
        'nx' : config['location'][0],
        'ny' : config['location'][1],
    }

    try:
        res = requests.get(url, params=params, timeout=4)
    except requests.exceptions.RequestException as e:
        raise Exception('API 호출 시간 초과.')

    if(res.status_code != 200):
        raise Exception('API 호출에 실패했습니다.')
    res_json = res.json()
    result_code = res_json['response']['header']['resultCode']

    if result_code != '00':
        raise Exception(api_err_translator(result_code))
    return res.json()
