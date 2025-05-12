#include <Wire.h>

const int SLAVE_ADDR = 8;

void setup() {
  Wire.begin();
  Serial.begin(9600);
}

void loop() {
  Wire.requestFrom(SLAVE_ADDR, 1);
  if (Wire.available()) {
    int val = Wire.read();
    if (val != 255) {
      Serial.print("✅ 슬레이브에서 버튼 ");
      Serial.print(val);
      Serial.println(" 눌림!");
    }
  }
  delay(100);
}
