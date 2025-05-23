# 👽 ALOM 부스 방어 시스템 – 재가동 부스 설명  

![Arduino](https://img.shields.io/badge/Arduino-00979D?style=flat&logo=arduino&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![3D Printing](https://img.shields.io/badge/3D_Printing-FF6F00?style=flat&logo=open3d&logoColor=white)  

기계식 키보드 버튼으로 총알에 맞았는지 상황을 감지 (불빛이 들어오는 자리로)  
→ 감지 후 점수 추가  
→ 게임이 끝나면 점수 고지 (아두이노 3대를 사용하며, 합계는 부스 담당자가 최종 계산)  

이 시스템은 2개의 아두이노를 I2C로 연결하여 12개의 과녁(버튼+전등)을 제어하며,  
PC에서는 UFO GUI를 통해 실시간으로 랜덤한 타겟을 제시하고  
정답 버튼을 누를 때까지 기다린 후 다음 타겟으로 넘어갑니다.

---

## 📁 파일 구조

```

alom-gun-game-arduino/  
├── README.md                 # 본 설명 파일  
├── .gitignore                # Git 옵션 설정  
├── 3d\_file/  
│   ├── OldVersions/
│   │   └── button\_3d(N).ipt  # 과거 인벤터 파일  
│   ├── button\_3d.ipt         # 키캡 인벤터 파일  
│   └── button\_3d.stl         # 3D 프린팅용 STL 파일  
├── arduino\_code_temp/
│   ├── master.ino            # 마스터 아두이노 (Serial ↔ I2C 중계)  
│   ├── slave.ino             # 슬레이브 아두이노 (각 4개 버튼+릴레이 제어)  
|   ├── main.py               # 메인 프로그램 python 파일
|   |   ├── ver1&temp  
|   |   |   ├──...            # 스위치 테스트 파일  
|   |   ├── test  
|   |   |   ├──...            # 프로그램 개조 & 파일  
├── arduino\_final/  
│   ├── light.ino            # 마스터 아두이노  
│   ├── button.ino             # 버튼용 아두이노  
|   ├── main.py               # 메인 프로그램 python 파일  

```

---

## ⚙️ 하드웨어 구성 및 포트 매핑

## 2. 버튼 아두이노 핀 매핑 (D2~D13)

| 핀 번호 | 버튼 번호 | 설명                    |
|---------|-----------|-------------------------|
| D2      | 1         | 버튼 1 (과녁 1)         |
| D3      | 2         | 버튼 2 (과녁 2)         |
| D4      | 3         | 버튼 3 (과녁 3)         |
| D5      | 4         | 버튼 4 (과녁 4)         |
| D6      | 5         | 버튼 5 (과녁 5)         |
| D7      | 6         | 버튼 6 (과녁 6)         |
| D8      | 7         | 버튼 7 (과녁 7)         |
| D9      | 8         | 버튼 8 (과녁 8)         |
| D10     | 9         | 버튼 9 (과녁 9)         |
| D11     | 10        | 버튼 10 (과녁 10)       |
| D12     | 11        | 버튼 11 (과녁 11)       |
| D13     | 12        | 버튼 12 (과녁 12)       |

*모두 `INPUT_PULLUP` 모드로 설정하고, 버튼 반대쪽은 GND에 연결하세요.*

---

## 3. 라이트 아두이노 핀 매핑 (D2~D13)

| 핀 번호 | 릴레이 번호 | 설명                              |
|---------|-------------|-----------------------------------|
| D2      | 1           | 릴레이 1 (과녁 1 전등)           |
| D3      | 2           | 릴레이 2 (과녁 2 전등)           |
| D4      | 3           | 릴레이 3 (과녁 3 전등)           |
| D5      | 4           | 릴레이 4 (과녁 4 전등)           |
| D6      | 5           | 릴레이 5 (과녁 5 전등)           |
| D7      | 6           | 릴레이 6 (과녁 6 전등)           |
| D8      | 7           | 릴레이 7 (과녁 7 전등)           |
| D9      | 8           | 릴레이 8 (과녁 8 전등)           |
| D10     | 9           | 릴레이 9 (과녁 9 전등)           |
| D11     | 10          | 릴레이 10 (과녁 10 전등)         |
| D12     | 11          | 릴레이 11 (과녁 11 전등)         |
| D13     | 12          | 릴레이 12 (과녁 12 전등)         |

*모두 `OUTPUT` 모드로 설정: `LOW`일 때 **전등 ON**, `HIGH`일 때 **전등 OFF** 상태입니다.*

---

## 🖥️ PC GUI 시스템 (UFO 타겟)

GUI 위치
|set 8 0  |set 8 1  |set 8 2  |
|---------|---------|---------|
|set 8 3  |set 9 0  |set 9 1  |
|set 9 2  |set 9 3  |set 10 1 |
|set 10 1 |set 10 2 |set 10 3 |


- **라이브러리**: [DearPyGui](https://github.com/hoffstadt/dearpygui)
- **동작 방식**:
  - 3x4 그리드에서 랜덤한 타겟 표시
  - 해당 타겟 정보를 마스터 아두이노로 전송
  - 정답 버튼이 눌릴 때까지 기다림
  - 버튼이 눌리면 다음 타겟으로 자동 진행

**초기 환경 설정으로 할 것**  

pip install setting
```
pip install dearpygui
pip install pyserial
```
  
python code edit
```
button_ser = serial.Serial('COM6', 9600, timeout=0.1)   #COM 포트 바꿔주기
relay_ser = serial.Serial('COM7', 9600, timeout=0.1)    #COM 포트 바꿔주기
```
  
---

## ⚠️ 주의사항

* 릴레이 모듈은 **LOW일 때 ON**, HIGH일 때 OFF입니다.
* **AC 전원과 연결 시 반드시 절연 조치** 필요합니다.
* 스위치 단독 테스트 시에는 **D2 + GND만 연결하여 확인** 가능합니다.
* 아두이노 간 I2C 통신 시 **GND도 반드시 공통으로 연결**해야 정상 작동합니다.

---
