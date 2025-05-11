#include <Wire.h>

const int SLAVE_ADDR = 8;  // 주소를 8, 9, 10으로 각각 바꿔서 업로드
const int buttonPins[4] = {2, 3, 4, 5};
const int relayPins[4]  = {6, 7, 8, 9};

int currentTarget = -1;
bool targetHit = false;

void setup() {
  Wire.begin(SLAVE_ADDR);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

  for (int i = 0; i < 4; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], HIGH); // 릴레이 OFF
  }
}

void loop() {
  if (currentTarget >= 0 && currentTarget < 4 && !targetHit) {
    if (digitalRead(buttonPins[currentTarget]) == LOW) {
      delay(50);
      while (digitalRead(buttonPins[currentTarget]) == LOW);
      targetHit = true;
      digitalWrite(relayPins[currentTarget], HIGH); // OFF
    }
  }
}

void receiveEvent(int howMany) {
  int cmd = Wire.read();
  if (cmd == 255) {
    // 모두 OFF
    for (int i = 0; i < 4; i++) digitalWrite(relayPins[i], HIGH);
    currentTarget = -1;
    targetHit = false;
  } else if (cmd >= 0 && cmd < 4) {
    currentTarget = cmd;
    targetHit = false;
    for (int i = 0; i < 4; i++) digitalWrite(relayPins[i], HIGH);
    digitalWrite(relayPins[currentTarget], LOW);
  }
}

void requestEvent() {
  Wire.write(targetHit ? 1 : 0);
}
#include <Wire.h>

const int SLAVE_ADDR = 8;  // ← 각각 9, 10으로 바꿔서 업로드
const int buttonPins[4] = {2, 3, 4, 5};
const int relayPins[4]  = {6, 7, 8, 9};

int currentTarget = -1;
bool targetHit = false;

void setup() {
  Wire.begin(SLAVE_ADDR);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

  for (int i = 0; i < 4; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], HIGH);  // 릴레이 OFF
  }
}

void loop() {
  if (currentTarget >= 0 && !targetHit) {
    if (digitalRead(buttonPins[currentTarget]) == LOW) {
      delay(50);
      while (digitalRead(buttonPins[currentTarget]) == LOW);
      targetHit = true;
      digitalWrite(relayPins[currentTarget], HIGH);  // OFF
    }
  }
}

void receiveEvent(int howMany) {
  int cmd = Wire.read();
  if (cmd == 255) {
    for (int i = 0; i < 4; i++) digitalWrite(relayPins[i], HIGH);
    currentTarget = -1;
    targetHit = false;
  } else if (cmd >= 0 && cmd < 4) {
    currentTarget = cmd;
    targetHit = false;
    for (int i = 0; i < 4; i++) digitalWrite(relayPins[i], HIGH);
    digitalWrite(relayPins[currentTarget], LOW);  // 릴레이 ON
  }
}

void requestEvent() {
  Wire.write(targetHit ? 1 : 0);
}
