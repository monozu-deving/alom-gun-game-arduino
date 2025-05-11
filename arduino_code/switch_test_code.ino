const int buttonPin = 2;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT_PULLUP);  // 내부 풀업 사용
}

int i = 0;

void loop() {
  i++;
  if (i > 10000) {
    i = 0;
  }
  if (digitalRead(buttonPin) == LOW) {
    Serial.println(i);
  delay(2);
  }
}
