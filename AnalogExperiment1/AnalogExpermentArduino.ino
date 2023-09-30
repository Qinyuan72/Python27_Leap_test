
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

String buffer;
int outputPin = 6;
int intBuffer;
int PWM_value;
char LCD_buffer[40];
char serialSentBuffer[20];
int analogCathode = A1;
int analogAnode = A0;

void setup() {
  Serial.begin(115200);
  pinMode(outputPin, OUTPUT);
  
  lcd.begin();
  lcd.backlight();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("AnalogExperiment");
}

void loop() {
  PWM_value = readSerialInput();
  analogWrite(outputPin, PWM_value);
  lcd.setCursor(0, 1);
  //sprintf(LCD_buffer, "PWM%dAc%dAn%d  ", PWM_value , analogRead(analogCathode),analogRead(analogAnode));
  //lcd.print(LCD_buffer);
  sprintf(serialSentBuffer, "S%d,%d,%d", PWM_value , analogRead(analogCathode),analogRead(analogAnode));
  Serial.print(serialSentBuffer);
}

int readSerialInput() {
  while (Serial.available() > 0) {
    buffer = Serial.readStringUntil('\n');
    intBuffer = buffer.toInt();
    return intBuffer;
  }
}