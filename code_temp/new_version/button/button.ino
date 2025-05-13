const int buttonPins[12] = {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 12; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
  }
}

void loop() {
  for (int i = 0; i < 12; i++) {
    if (digitalRead(buttonPins[i]) == LOW) {
      if (digitalRead(buttonPins[i]) == LOW) {
        while (digitalRead(buttonPins[i]) == LOW);
        Serial.println(i + 1); // 버튼 번호 (1~12) 전송
      }
    }
  }
}