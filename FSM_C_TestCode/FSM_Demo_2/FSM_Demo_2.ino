#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
const uint8_t bit0 = 2;         // GREEN_LED is connected to D13
const uint8_t bit1 = 4;        // YELLOW_LED is connected to D12
const uint8_t bit2 = 6;           // RED_LED is connected to D11
const uint8_t bit3 = 8;               // SW1 is connected to D10
int serialReadInt;
enum states {  // Define enumerated type for state machine states
  ZERO,
  ONE,
  TWO,
  THREE,
  FOUR,
  FIVE,
  SIX,
  SEVEN,
  EIGHT,
  RESET_TO_ZERO,
};

states state;                         // Global variable to store current state

void setup()
{
  pinMode(2, OUTPUT);         // Configure GREEN_LED pin as a digital output
  pinMode(4, OUTPUT);        // Configure YELLOW_LED pin as a digital output
  pinMode(6, OUTPUT);           // Configure RED_LED pin as a digital output
  pinMode(8, OUTPUT);
  Serial.begin(115200);

  lcd.begin();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("FSM_Demo_2");
  state = ZERO;
}


void loop() {

  switch (state) {
    case ZERO:
      digitalWrite(bit0, 0);
      digitalWrite(bit1, 0);
      digitalWrite(bit2, 0);
      digitalWrite(bit3, 0);

      lcd.setCursor(0, 0);
      lcd.print("FSM_Demo_2");
      lcd.setCursor(0, 1);
      lcd.print("ZERO");

      serialReadInt = serialRead();

      if (serialReadInt == 1) {
        state = ONE;
        lcd.print("->ONE");
      }
      else if (serialReadInt == 2) {
        state = TWO;
        lcd.print("->TWO");
      }
      else if (serialReadInt == 3) {
        state = THREE;
        lcd.print("->FOUR");
      }
      else if (serialReadInt == 4) {
        state = FOUR;
        lcd.print("->FOUR");
      }
      else if (serialReadInt == 5) {
        state = FIVE;
        lcd.print("->FIVE");
      }
      else if (serialReadInt == 6) {
        state = SIX;
        lcd.print("->SIX");
      }
      else if (serialReadInt == 7) {
        state = SEVEN;
        lcd.print("->SEVEN");
      }
      else if (serialReadInt == 8) {
        state = EIGHT;
        lcd.print("->EIGHT");
      }
      else {
        state = ZERO;
      }
      break;

    case ONE:
      digitalWrite(bit0, 1);
      digitalWrite(bit1, 0);
      digitalWrite(bit2, 0);
      digitalWrite(bit3, 0);
      lcd.setCursor(0, 0);
      lcd.print("Send'$9'to rest");
      if (serialRead() == 9) {
        state = ZERO;
        lcd.clear();
      }
      break;

    case TWO:
      digitalWrite(bit0, 0);
      digitalWrite(bit1, 1);
      digitalWrite(bit2, 0);
      digitalWrite(bit3, 0);
      lcd.setCursor(0, 0);
      lcd.print("Send'$9'to rest");
      if (serialRead() == 9) {
        state = ZERO;
        lcd.clear();
      }
      break;

    case THREE:
      digitalWrite(bit0, 1);
      digitalWrite(bit1, 1);
      digitalWrite(bit2, 0);
      digitalWrite(bit3, 0);
      lcd.setCursor(0, 0);
      lcd.print("Send'$9'to rest");
      if (serialRead() == 9) {
        state = ZERO;
        lcd.clear();
      }
      break;
    case FOUR:
      digitalWrite(bit0, 0);
      digitalWrite(bit1, 0);
      digitalWrite(bit2, 1);
      digitalWrite(bit3, 0);
      lcd.setCursor(0, 0);
      lcd.print("Send'$9'to rest");
      if (serialRead() == 9) {
        state = ZERO;
        lcd.clear();
      }
      break;
    case FIVE:
      digitalWrite(bit0, 1);
      digitalWrite(bit1, 0);
      digitalWrite(bit2, 1);
      digitalWrite(bit3, 0);
      lcd.setCursor(0, 0);
      lcd.print("Send'$9'to rest");
      if (serialRead() == 9) {
        state = ZERO;
        lcd.clear();
      }
      break;
    case SIX:
      digitalWrite(bit0, 0);
      digitalWrite(bit1, 1);
      digitalWrite(bit2, 1);
      digitalWrite(bit3, 0);
      lcd.setCursor(0, 0);
      lcd.print("Send'$9'to rest");
      if (serialRead() == 9) {
        state = ZERO;
        lcd.clear();
      }
      break;
    case SEVEN:
      digitalWrite(bit0, 1);
      digitalWrite(bit1, 1);
      digitalWrite(bit2, 1);
      digitalWrite(bit3, 0);
      lcd.setCursor(0, 0);
      lcd.print("Send'$9'to rest");
      if (serialRead() == 9) {
        state = ZERO;
        lcd.clear();
      }
      break;
    case EIGHT:
      digitalWrite(bit0, 0);
      digitalWrite(bit1, 0);
      digitalWrite(bit2, 0);
      digitalWrite(bit3, 1);
      lcd.setCursor(0, 0);
      lcd.print("Send'$9'to rest");
      if (serialRead() == 9) {
        state = ZERO;
        lcd.clear();
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
      Serial.println(c);
    }
  }
}
