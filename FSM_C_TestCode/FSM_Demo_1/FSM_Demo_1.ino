#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

enum states {  // Define enumerated type for state machine states
  ZERO,
  ONE,
  TWO,
  THREE
};

states state;                         // Global variable to store current state

void setup()
{
  Serial.begin(115200);

  lcd.begin();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("FSM Demo");
  delay(1000);
  state = ZERO;
}


void loop() {

  switch (state) {
    case ZERO:
      lcd.setCursor(0, 1);
      lcd.print("0");
      if (serialRead() == 1) {
        state = ONE;
        lcd.setCursor(0, 1);
        lcd.print("1");
      }
      break;

    case ONE:
      if (serialRead() == 1) {
        state = TWO;
        lcd.setCursor(0, 1);
        lcd.print("2");
      }
      break;

    case TWO:
      if (serialRead() == 1) {
        state = THREE;
        lcd.setCursor(0, 1);
        lcd.print("3");
      }
      break;

    case THREE:
      if (serialRead() == 1) {  
        state = ZERO;
        lcd.setCursor(0, 1);
        lcd.print("0");
      }
      break;
  }
}

int serialRead() {
  while (Serial.available() > 0)
  {
    char c = Serial.read();
    if (c == '$')
    {
      Serial.println("'$'Received");
      char c = Serial.read();
      c = c - 48;
      return c;
    }
  }
}
