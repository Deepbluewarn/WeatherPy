import json

config = None
init = False

# 설정 파일을 읽어오거나 생성합니다.

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    config = {}
    init = True
    with open('config.json', 'w') as f:
        json.dump(config, f)
except json.JSONDecodeError:
    print("Error: Could not decode the config file. Please check its format.")
