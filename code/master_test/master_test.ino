#include <Wire.h>

const int slaveAddresses[] = {8, 9, 10};

void setup() {
  Wire.begin();             // 마스터 모드
  Serial.begin(9600);       // PC에 출력
}

void loop() {
  for (int i = 0; i < 3; i++) {
    int addr = slaveAddresses[i];/
    Wire.requestFrom(addr, 1);  // 슬레이브에 버튼 눌림 여부 요청
    if (Wire.available()) {
      int response = Wire.read();
      if (response == 1) {
        Serial.print("버튼 눌림 from 슬레이브 ");
        Serial.println(addr);
      }
    }
  }
  delay(100); // 너무 빠르게 요청하지 않도록
}
