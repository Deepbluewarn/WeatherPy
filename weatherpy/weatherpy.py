from rich import print
import json
from rich.prompt import Prompt
import fullscreen.fullscreen as fs

config = {}
init = False

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    init = True
except json.JSONDecodeError:
    print("Error: 설정 파일을 불러오는 중 문제가 발생했습니다. 설정 파일을 삭제하고 다시 실행해주세요.")

# 설정 파일이 없는 경우, 사용자에게 설정을 입력받습니다.

if init == True:
    print("WeatherPy 를 처음 실행하셨군요! 기본 설정을 진행합니다.")
    location = Prompt.ask("지역을 입력하세요. (예: Seoul, KR)")

    config['location'] = location

    with open('config.json', 'w') as f:
        json.dump(config, f)

if __name__ == "__main__": 
    fs.initScreen()
    print("WeatherPy is running...")
