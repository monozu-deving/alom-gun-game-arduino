#include <Wire.h>

const int SLAVE_ADDR = 8;  // 슬레이브 주소 (8, 9, 10 등)
const int buttonPins[4] = {2, 3, 4, 5};
const int relayPins[4]  = {6, 7, 8, 9};
int currentTarget = -1;     // 마스터가 지정한 타겟 인덱스
int pressedIndex = -1;      // 실제 눌린 버튼 인덱스

void setup() {
  Wire.begin(SLAVE_ADDR);
  Wire.onReceive(receiveEvent);  // SET 명령 수신
  Wire.onRequest(requestEvent);  // 버튼 상태 요청

  for (int i = 0; i < 4; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], HIGH); // 릴레이 OFF
  }
}

void loop() {
  for (int i = 0; i < 4; i++) {
    if (digitalRead(buttonPins[i]) == LOW) {
      delay(50); // 디바운스
      if (digitalRead(buttonPins[i]) == LOW) {
        pressedIndex = i;
        digitalWrite(relayPins[i], HIGH);  // 눌렸으니 해당 릴레이 OFF
        break;  // 한 번에 하나만 감지
      }
    }
  }
}

void receiveEvent(int howMany) {
  int cmd = Wire.read();  // 마스터가 보낸 인덱스
  for (int i = 0; i < 4; i++) {
    digitalWrite(relayPins[i], HIGH);  // 모든 릴레이 OFF
  }

  if (cmd >= 0 && cmd < 4) {
    currentTarget = cmd;
    digitalWrite(relayPins[cmd], LOW);  // 해당 릴레이 ON
  }
}

void requestEvent() {
  if (pressedIndex >= 0 && pressedIndex < 4) {
    Wire.write(pressedIndex);  // 어떤 버튼이든 보고
    pressedIndex = -1;         // 보고한 후 초기화
  } else {
    Wire.write(255);           // 아무것도 안 눌렸으면 255
  }
}
