#include <Wire.h>

const int SLAVE_ADDR = 8;
const int buttonPins[4] = {2, 3, 4, 5};

int pressedIndex = -1;

void setup() {
  Wire.begin(SLAVE_ADDR);
  Wire.onRequest(requestEvent);
  Serial.begin(9600);

  for (int i = 0; i < 4; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }
}

void loop() {
  if (pressedIndex == -1) {
    for (int i = 0; i < 4; i++) {
      if (digitalRead(buttonPins[i]) == LOW) {
        delay(30);
        if (digitalRead(buttonPins[i]) == LOW) {
          while (digitalRead(buttonPins[i]) == LOW);  // 버튼 떼기 대기
          pressedIndex = i;
          Serial.print("🔘 버튼 ");
          Serial.print(i);
          Serial.println(" 눌림");
          break;
        }
      }
    }
  }
}

void requestEvent() {
  if (pressedIndex != -1) {
    Wire.write(pressedIndex);  // 0~3 중 눌린 버튼 번호 전송
    pressedIndex = -1;         // 한번 보낸 후 초기화
  } else {
    Wire.write(255);  // 아무 버튼도 안 눌렸으면 255 전송
  }
}
