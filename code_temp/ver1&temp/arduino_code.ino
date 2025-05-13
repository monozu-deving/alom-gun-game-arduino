#include <Arduino.h>

const int buttonPins[4] = {2, 3, 4, 5};    // 버튼 핀
const int relayPins[4]  = {6, 7, 8, 9};    // 릴레이 핀 (전등 제어)
int activeIndex = -1;                     // 현재 불이 들어온 전등 인덱스
int score = 0;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 4; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], HIGH);  // 릴레이 OFF (LOW일 때 켜짐)
  }

  randomSeed(analogRead(A0));  // 무작위 시드 설정
  activateRandomLight();       // 시작 시 무작위 전등 점등
}

void activateRandomLight() {
  if (activeIndex != -1) {
    digitalWrite(relayPins[activeIndex], HIGH); // 이전 전등 OFF
  }
  activeIndex = random(0, 4);
  digitalWrite(relayPins[activeIndex], LOW);    // 새로운 전등 ON
  Serial.print("New target: ");
  Serial.println(activeIndex + 1);
}

void loop() {
  for (int i = 0; i < 4; i++) {
    if (digitalRead(buttonPins[i]) == LOW) {
      delay(50);  // 디바운스
      while (digitalRead(buttonPins[i]) == LOW); // 버튼 뗄 때까지 대기

      if (i == activeIndex) {
        score++;
        Serial.print("Correct! Score: ");
        Serial.println(score);
        activateRandomLight();  // 다음 문제로
      } else {
        Serial.println("Wrong button.");
      }
    }
  }
}
