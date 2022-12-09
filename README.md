# 세컨블록 블록 관리 툴

## 세컨블록

### 개요
[세컨블록](https://2ndblock.com)은 한국의 가상자산 거래소인 [업비트](https://upbit.com)의 운영사 두나무에서 운영중인 메타버스 플랫폼이다.  
픽셀 감성이 묻어나는 나만의 공간에서 나의 개성과 취향이 담긴 캐릭터를 이용해 다양한 사람들과 더 즐겁고 특별하게 소통할 수 있는 공간이다.

### 챌린지
> 어떠한 행동을 취한 것을 인증한 후, 다음 주자를 지목하여 의도한 행동을 유행시키는 일종의 마케팅 방식.

세컨블록의 챌린지란 [나무위키](https://namu.wiki)의 [챌린지](https://namu.wiki/w/%EC%B1%8C%EB%A6%B0%EC%A7%80#s-3.4) 문서 3.4 항목에 서술되어 있는 용례라고 볼 수 있다.  
세컨블록 이용 활성화를 위해 두나무에서 이벤트성 마케팅을 챌린지 형태로 진행하고 있다. 

| 챌린지명                | 기간                           | 주소    |
|-----------------------|------------------------------|-------|
| 대학생 인싸 챌린지         | 2022년 9월 29일 ~ 2022년 10월 21일 | https://2ndblock.com/events/inssa  |
| 방구석 전문가 메타버스 챌린지 | 2022년 12월 5일 ~ 2023년 1월 6일   | https://2ndblock.com/events/expert  |

## 프로젝트

### 개요
세컨블록 챌린지는 상금으로 비트코인을 받을 수 있고, 대학생 인싸 챌린지의 경우는 1등을 한 경우 두나무 메타버스실 인턴 지원시 서류전형 면제라는 매우 메리트가 큰 이벤트이다.  
챌린지 우승을 위해 방 개념인 **블록**에서 세컨블록 유저들이 팔로우와 방명록 작성을 하도록 유도하는 행사들을 기획하였고  
원할한 행사 운영과 부실한 세컨블록의 기능을 극복하기 위해 별도의 블록 관리 프로그램(툴)을 만들어 챌린지에 참여중이다.

### 행사 기획
#### 대학생 인싸 챌린지
대학생 인싸 챌린지에서는 [전용 블록](https://2ndblock.com/room/kqlm15NawUT9X1a5vOQm) 에서 차트출력, 모의경매, 티커출력 기능을 사용한다. 해당하는 툴은 [inssa.py](./inssa.py)이다.

| 행사명 | 날짜 | 내용                                                                                    |
|-----------------|-----------------|---------------------------------------------------------------------------------------|
| 업비트 NFT 모의경매 | 2022년 10월 12일 | 업비트 NFT 수집가인 흑우촌이 보유중인 NFT 작품을 단순히 전시하는 것을 넘어 가상의 포인트로 모의경매 게임을 진행                    |
| 흑우촌 메타버스 AMA | 2022년 10월 15일 | 정식 공개 예정인 메타버스 커뮤니티 [흑우촌](https://heuguchon.com)에 대한 궁금증을 해소하는 무엇이든 물어보세요 행사인 AMA를 진행 |

#### 방구석 전문가 메타버스 챌린지
방구석 전문가 메타버스 챌린지에서는 [전용 블록](https://2ndblock.com/room/yqDNWHh3xNLAsBO4mNEv) 에서 지갑 화이트리스트 등록 기능을 사용한다. 해당하는 툴은 [expert.py](./expert.py)이다.

| 행사명                           | 날짜             | 내용                                                                                      |
|-------------------------------|----------------|-----------------------------------------------------------------------------------------|
| 흑우촌 관련 행사 참석 기념 NFT 화이트리스트 접수 | 2022년 12월 6일 ~ | 앞의 대학생 인싸 챌린지의 두 행사에 참여한 흑우촌 커뮤니티 지지자분들께 감사의 마음을 담아 참석기념 NFT를 증정하고자 이더리움 지갑 주소를 접수받고 있음 |

### 기능
| 기능명 | 주요기술 | 내용 | 예시 |
|----|----------|-----| ---- |
| 차트 출력 | Selenium | 세컨블록의 화상공유 또는 스크린공유 기능을 통해 블록에 있는 유저가 전체 채팅창에서 특정 종목을 입력하면 업비트 거래소에서 해당 종목의 차트를 출력한다.</br>ex) '**/종목변경** BTC/KRW' | ![차트출력예시](./assets/feature_chart.png) |
| 모의 경매 | Selenium, Flask | 세컨블록의 화상공유 또는 스크린공유 기능을 통해 현재 경매 상황을 볼 수 있고, 블록에 있는 유저가 채팅 커맨드로 경매 게임에 참여할 수 있다.</br></br>**경매규칙**</br>참가자들은 각자 가상의 포인트인 1,000,000 HD를 지급 받아, 소지금 내에서 출품된 작품들을 입찰할 수 있다.</br></br>채팅 명령어로 입찰에 참여할 수 있으며, 실제 경매장과 같이 경매 상황을 실시간으로 관전할 수 있다.</br></br>**채팅 명령어**</br>1. **/등록**</br>모의경매 참여에 필요한 가상의 포인트를 지급받는다.</br>2. **/입찰** (금액)</br>입찰 진행중인 작품을 얼마에 입찰할 것인지 입찰의사를 밝힌다.</br></br>**운영**</br>모의경매는 로컬 컴퓨터의 메모리만 사용하기 때문에 별도의 DB 구축이 필요없다.</br>다음의 명령들을 입력하여 모의경매 서버를 먼저 활성화한다.</br>1. `cd auction`</br>2. `flask run --port 8000`</br>3. `curl http://localhost:8000/init` </br>그 다음에는 블록내에 접속하여 'auction/screen.html'을 웹 브라우저로 실행하여 세컨블록의 화상공유 또는 스크린공유를 통해 경매 상황판을 출력한다.</br>본격적인 경매 진행은 채팅 커맨드로 사회자가 경매를 진행하면 된다.</br>1. **/경매시작** (입찰 하한가)</br>해당 작품의 경매를 시작하면서 입찰 제한가를 지정한다.</br>2. **/경매종료**</br>해당 작품의 경매를 종료하여 낙찰자를 선정한다.</br>3. **/다음경매**</br>다음 작품으로 경매를 진행시킨다. | ![모의경매예시](./assets/feature_auction.jpg) | 
| 티커 출력 | Selenium, OpenCV, NumPy | 세컨블록의 블록 꾸미기 기능을 자동화하여 업비트 거래소의 비트코인 시세와 USDT(BTC/KRW / BTC/USDT) 시세를 출력한다.</br></br>블록내에 있는 특정 아이템(Canvas)들을 이미지 기반으로 인식하여 오브젝트의 중심 좌표를 찾고, 일차식을 만들어 수학적으로 아이템들이 존재할 수 있는 영역을 계산한다. 그 다음에는 오브젝트가 나타내야할 숫자가 다른경우 그 오브젝트를 지우고, 블록 꾸미기 기능에 있는 대응되는 오브젝트를 생성하여 원래 자리에 배치한다.</br></br>**주의사항**</br>원할한 이미지 인식을 위해 Selenium이 구동되는 컴퓨터의 해상도는 4K(3840 x 2160)를 권장함.</br></br>**참고자료**</br>[ticker/graphical.py](./ticker/graphical.py)에 있는 소스코드는 [HTML \<canvas\> testing with Selenium and OpenCV](https://www.linkedin.com/pulse/html-canvas-testing-selenium-opencv-maciej-kusz) 글을 토대로 가져와 사용하였다. | ![티커출력예시](./assets/feature_ticker.png) |
| 지갑 화이트리스트 등록 | Selenium, Flask, MariaDB | 세컨블록 내에서 귓속말 기능을 통해 이더리움 지갑 주소를 화이트리스트 처리한다. | ![화이트리스트예시](./assets/feature_whitelist.png) |

### 설치
Python 3 인터프리터가 있는 환경에서
```console
python -m venv ./venv
pip install -r requirements.txt
```

## 실적
### 대학생 인싸 챌린지
* 명예의 전당(2등)
![명예의 전당](./assets/hall_of_fame.png)

* 시상관련 이메일
![시상관련 이메일](./assets/email.png)

## 도움을 주신 분들
대학생 인싸 챌린지에서 같이 팀으로 참여하여 2등이라는 결과를 같이 만들어준 트비, 차가운불, 진토리, 로우나01님께 감사드립니다.

## 라이선스
이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](./LICENSE) 파일을 확인하세요.

### 오픈소스 라이선스
* [Selenium](https://www.selenium.dev/documentation/about/copyright/#license)  
Apache License 2.0  
* [OpenCV](https://opencv.org/license/)  
Apache License 2.0
* [Flask](https://flask.palletsprojects.com/en/2.2.x/license/)  
3-Clause BSD License
* [NumPy](https://numpy.org/doc/stable/license.html)  
3-Clause BSD License