char cmd;
const int relay1 = 2;
const int relay2 = 3;
const int relay3 = 4;
const int relay4 = 5;
const int relay5 = 6;
const int relay6 = 7;
const int relay7 = 8;
const int relay8 = 9;
const int relay9 = 10;
const int relay10 = 11;
const int relay11 = 12;
const int relay12 = 13;
int currentTarget = -1;

void setup() {
  Serial.begin(9600);
  pinMode(relay1, OUTPUT); digitalWrite(relay1, HIGH);
  pinMode(relay2, OUTPUT); digitalWrite(relay2, HIGH);
  pinMode(relay3, OUTPUT); digitalWrite(relay3, HIGH);
  pinMode(relay4, OUTPUT); digitalWrite(relay4, HIGH);
  pinMode(relay5, OUTPUT); digitalWrite(relay5, HIGH);
  pinMode(relay6, OUTPUT); digitalWrite(relay6, HIGH);
  pinMode(relay7, OUTPUT); digitalWrite(relay7, HIGH);
  pinMode(relay8, OUTPUT); digitalWrite(relay8, HIGH);
  pinMode(relay9, OUTPUT); digitalWrite(relay9, HIGH);
  pinMode(relay10, OUTPUT); digitalWrite(relay10, HIGH);
  pinMode(relay11, OUTPUT); digitalWrite(relay11, HIGH);
  pinMode(relay12, OUTPUT); digitalWrite(relay12, HIGH);
}

void loop() {
  if (Serial.available()) {
    cmd = Serial.read();
    // 모든 릴레이 OFF (HIGH)
    digitalWrite(relay1, HIGH);
    digitalWrite(relay2, HIGH);
    digitalWrite(relay3, HIGH);
    digitalWrite(relay4, HIGH);
    digitalWrite(relay5, HIGH);
    digitalWrite(relay6, HIGH);
    digitalWrite(relay7, HIGH);
    digitalWrite(relay8, HIGH);
    digitalWrite(relay9, HIGH);
    digitalWrite(relay10, HIGH);
    digitalWrite(relay11, HIGH);
    digitalWrite(relay12, HIGH);

    // cmd에 따라 해당 릴레이만 ON (LOW)
    if (cmd == '1')      digitalWrite(relay1, LOW);
    else if (cmd == '2') digitalWrite(relay2, LOW);
    else if (cmd == '3') digitalWrite(relay3, LOW);
    else if (cmd == '4') digitalWrite(relay4, LOW);
    else if (cmd == '5') digitalWrite(relay5, LOW);
    else if (cmd == '6') digitalWrite(relay6, LOW);
    else if (cmd == '7') digitalWrite(relay7, LOW);
    else if (cmd == '8') digitalWrite(relay8, LOW);
    else if (cmd == '9') digitalWrite(relay9, LOW);
    else if (cmd == 'a') digitalWrite(relay10, LOW); // 10
    else if (cmd == 'b') digitalWrite(relay11, LOW); // 11
    else if (cmd == 'c') digitalWrite(relay12, LOW); // 12
  }
}