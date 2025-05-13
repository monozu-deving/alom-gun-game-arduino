const int relayPins[4] = {6, 7, 8, 9};

void setup() {
  for (int i = 0; i < 4; i++) {
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], HIGH);  // 모두 OFF로 시작
  }
}

void loop() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(relayPins[i], LOW);   // 릴레이 ON
    delay(1000);                       // 1초 대기
    digitalWrite(relayPins[i], HIGH);  // 릴레이 OFF
    delay(500);                        // 0.5초 대기
  }
}
