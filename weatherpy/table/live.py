from datetime import datetime
from tools.translator import SKY_translator, PTY_translator, weekday_translator
import pandas as pd
from collections import Counter
from rich.console import Console
from rich.table import Table
from api.short_term.shortTerm import getShortTermWeatherInfo
import pytz
# 단기 예보를 조회한 다음 가장 최근의 예보 데이터를 테이블로 출력

def tableLive() -> Table:
    korea = pytz.timezone('Asia/Seoul')
    date = datetime.now(korea).strftime('%Y%m%d')
    time = datetime.now(korea).strftime('%H') + '00'
    res = getShortTermWeatherInfo(date = date)
    items = res['response']['body']['items']['item']

    base_dates = []
    base_times = []
    categories = []
    fcst_dates = []
    fcst_times = []
    fcst_values = []
    nx = []
    ny = []

    for item in items:
        base_dates.append(item['baseDate'])
        base_times.append(item['baseTime'])
        fcst_dates.append(item['fcstDate'])
        fcst_times.append(item['fcstTime'])
        fcst_values.append(item['fcstValue'])
        nx.append(item['nx'])
        ny.append(item['ny'])
        categories.append(item['category'])
    
    res = pd.DataFrame({
        'base_date' : base_dates,
        'base_time' : base_times,
        'category' : categories,
        'fcst_date' : fcst_dates,
        'fcst_time' : fcst_times,
        'fcst_value' : fcst_values,
        'nx' : nx,
        'ny' : ny
    })

    mask = res[(res['fcst_date'] == date) & (res['fcst_time'] == time)]

    pivot = mask.pivot(index='fcst_time', columns='category', values='fcst_value')
    table = Table(title="현재 날씨")

    table.add_column("기온", justify="center", style="cyan", no_wrap=True)
    table.add_column("강수 확률", justify="center", style="magenta", no_wrap=True)
    table.add_column("습도", justify="center", style="green", no_wrap=True)
    table.add_column("풍속", justify="center", style="yellow", no_wrap=True)
    table.add_column("하늘 상태", justify="center", style="blue", no_wrap=True)
    table.add_column("강수 형태", justify="center", style="red", no_wrap=True)
    
    try:
        table.add_row(
            f"{pivot['TMP'].tolist()[0]}°C",
            f"{pivot['POP'].tolist()[0]}%",
            f"{pivot['REH'].tolist()[0]}%",
            f"{pivot['WSD'].tolist()[0]}m/s",
            SKY_translator(int(pivot['SKY'].tolist()[0])),
            PTY_translator(int(pivot['PTY'].tolist()[0]))
        )
    except Exception as e:
        print(e)
    return table
