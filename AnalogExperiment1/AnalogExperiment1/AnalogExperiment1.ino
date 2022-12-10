String buffer;
int testPWM = 6;
int intBuffer;
int PWM_value;
void setup() {
  Serial.begin(115200);
  pinMode(testPWM, OUTPUT);
}

void loop() {
  PWM_value = readSerialInput();
  analogWrite(testPWM,PWM_value);
}

int readSerialInput() {
  while (Serial.available() > 0) {
    buffer = Serial.readStringUntil('\n');
    intBuffer = buffer.toInt();
    return intBuffer;
  }
}
