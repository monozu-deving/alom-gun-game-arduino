#include <Wire.h>
// test file
const int slaveAddresses[] = {8, 9, 10};

void setup() {
  Wire.begin();
  Serial.begin(9600);
}

void loop() {
  for (int i = 0; i < 3; i++) {
    int addr = slaveAddresses[i];
    Wire.requestFrom(addr, 1);
    if (Wire.available()) {
      int val = Wire.read();
      if (val != 255) {
        // 포맷: 슬레이브주소:버튼번호
        Serial.print("HIT ");
        Serial.print(addr);
        Serial.print(" ");
        Serial.println(val);
      }
    }
  }
  delay(100);
}
