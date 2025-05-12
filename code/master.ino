#include <Wire.h>

void setup() {
  Wire.begin();       // 마스터 시작
  Serial.begin(9600); // Python과 Serial 통신
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');

    if (cmd.startsWith("SET")) {
      int addr = cmd.substring(4, 5).toInt();
      int idx = cmd.substring(6).toInt();
      Wire.beginTransmission(addr);
      Wire.write(idx);
      Wire.endTransmission();
      Serial.println("OK");
    }

    if (cmd.startsWith("SET")) {
      int space = cmd.indexOf(' ', 4);
      int addr = cmd.substring(4, space).toInt();
      int idx = cmd.substring(space + 1).toInt();
      Wire.beginTransmission(addr);
      Wire.write(idx);
      Wire.endTransmission();
      Serial.println("OK");
    }
  }
}
