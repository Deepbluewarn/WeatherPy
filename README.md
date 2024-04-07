# WeatherPy

동의대학교 데이터과학프로그래밍 과제 프로젝트

기상청 API를 활용하여 날씨 데이터를 받아 날씨 출력 및 기초적인 통계 자료를 생성합니다.

## 주요 기능

 - 예보 조회
 - 날씨 데이터를 활용한 통계 자료 생성
 - ChatGPT API를 활용한 날씨 요약 및 조언 기능

## 사용 기술

 - [python](https://www.python.org/)
 - [rich](https://github.com/Textualize/rich)

## 설치
```
git clone https://github.com/Deepbluewarn/WeatherPy
```
## 사용법

이 프로젝트는 [poetry](https://python-poetry.org/)로 의존성 관리와 패키징을 수행합니다.

poetry 설치 후 프로젝트 디렉토리로 이동한 다음 아래 명령을 실행합니다.

```bash
poetry install
poetry run python weatherpy/weatherpy.py
```

## 스크린샷

### TODO

 - 기상청 API 격자 파일을 csv로 변환한 다음 사용자의 선택을 설정 파일에 저장하는 기능 구현

 - 기상청에서 제공하는 '초단기실황', '초단기예보' API 를 활용해서 현재 날씨를 출력하는 기능 구현.
   
 - 기상청 종관기상관측 API로 그래프 등 통계 자료를 생성하는 기능 구현


