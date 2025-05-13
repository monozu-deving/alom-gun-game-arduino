#include <Wire.h>

const int slaveAddresses[] = {8, 9, 10};  // 연결된 슬레이브 주소들 (필요 시 확장 가능)

void setup() {
  Wire.begin();             // 마스터 시작
  Serial.begin(9600);       // 파이썬과 시리얼 통신
}

void loop() {
  // 파이썬에서 SET 명령을 받을 경우
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd.startsWith("SET")) {
      int slave = -1, index = -1;
      if (sscanf(cmd.c_str(), "SET %d %d", &slave, &index) == 2) {
        Wire.beginTransmission(slave);
        Wire.write(index);
        Wire.endTransmission();
      }
    }
  }

  // 슬레이브들로부터 버튼 입력 체크
  for (int i = 0; i < 3; i++) {
    int addr = slaveAddresses[i];
    Wire.requestFrom(addr, 1);
    if (Wire.available()) {
      int val = Wire.read();
      if (val >= 0 && val < 4) {
        int buttonNumber = (addr - 8) * 4 + val + 1;
        Serial.println(buttonNumber);  // 파이썬으로 전송
      }
    }
  }

  delay(50);  // 너무 빠르게 반복하지 않도록
}
