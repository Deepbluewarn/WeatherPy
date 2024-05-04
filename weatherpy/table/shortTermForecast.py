from datetime import datetime
from tools.translator import SKY_translator, PTY_translator, weekday_translator
import pandas as pd
from collections import Counter
from rich.console import Console
from rich.table import Table
from api.short_term.shortTerm import getShortTermWeatherInfo

# 단기 예보를 조회한 다음 결과를 테이블로 출력

def tableSTFcst() -> Table:
    res = getShortTermWeatherInfo(date = datetime.now().strftime('%Y%m%d'))
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

    grouped = res.groupby(['fcst_date'])

    res_days = []
    res_skies = []
    res_temps = []
    res_pty = []

    for name, group in grouped:
        pivot_table = group.pivot(index='fcst_time', columns='category', values='fcst_value')

        res_days.append(name[0])

        try:
            sky_values = pivot_table['SKY'].tolist()
        except:
            sky_values = []

        try:
            pty_values = pivot_table['PTY'].tolist()
        except:
            pty_values = []
        
        try:
            temp_min_values = pivot_table['TMN'].tolist()
            temp_max_values = pivot_table['TMX'].tolist()
        except:
            temp_min_values = ['-']
            temp_max_values = ['-']

        counter = Counter(sky_values)
        most_common_value = counter.most_common(1)[0][0]
        res_skies.append(most_common_value)

        pty_values = [x for x in pty_values if x != '0']

        counter = Counter(pty_values)

        if len(pty_values) == 0:
            most_common_value = '0'
        else:
            most_common_value = counter.most_common(1)[0][0]
            
        res_pty.append(most_common_value)

        temp_max_values = [x for x in temp_max_values if type(x) == str]
        temp_min_values = [x for x in temp_min_values if type(x) == str]
        
        res_temps.append({
            'min': min(temp_min_values),
            'max': max(temp_max_values)
        })

    weather_df = pd.DataFrame({
        'date': res_days,
        'sky': res_skies,
        'temp': res_temps,
        'pty': res_pty
    })
    
    table = Table(title="단기 예보 조회")

    try:
        for _ in range(weather_df['date'].size):
            date = datetime.strptime(weather_df['date'][_], '%Y%m%d')
            weekday_num = date.weekday()
            table.add_column(f'{date.day}일 ({weekday_translator(weekday_num)})', justify="center")

        sky_list = map(SKY_translator, map(int, weather_df['sky'].to_list()))

        table.add_row(*sky_list)
        table.add_row(*weather_df['temp'].apply(lambda x: f"{x['min']}° / {x['max']}°").to_list())
        table.add_row(*map(PTY_translator, map(int, (weather_df['pty'].to_list()))))
    except Exception as e:
        table.add_row(e)

    return table
