#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
const uint8_t bit0 = 2; // GREEN_LED is connected to D13
const uint8_t bit1 = 4; // YELLOW_LED is connected to D12
const uint8_t bit2 = 6; // RED_LED is connected to D11
const uint8_t bit3 = 8; // SW1 is connected to D10
int serialReadInt;
enum states
{ // Define enumerated type for state machine states
  ZERO,
  ONE,
  TWO,
  THREE,
  FOUR,
  FIVE,
  SIX,
  SEVEN,
  EIGHT,
  NINE,
  TEN,
  ELEVEN,
  TWIVE,
  TWELVE,
  THIRTEEN,
  FOURTEEN,
  FIFTEEN,
  SIXTEEN,
};

states state; // Global variable to store current state

void setup()
{
  pinMode(bit0, OUTPUT);
  pinMode(bit1, OUTPUT);
  pinMode(bit2, OUTPUT);
  pinMode(bit3, OUTPUT);
  Serial.begin(115200);

  lcd.begin();
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("FSM_Demo_2 '$i'");
  state = ZERO;
}

void loop()
{

  switch (state)
  {
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

      if (serialReadInt == 1)
      {
        state = ONE;
        lcd.print("->ONE");
      }
      else if (serialReadInt == 2)
      {
        state = TWO;
        lcd.print("->TWO");
      }
      else if (serialReadInt == 3)
      {
        state = THREE;
        lcd.print("->THREE");
      }
      else if (serialReadInt == 4)
      {
        state = FOUR;
        lcd.print("->FOUR");
      }
      else if (serialReadInt == 5)
      {
        state = FIVE;
        lcd.print("->FIVE");
      }
      else if (serialReadInt == 6)
      {
        state = SIX;
        lcd.print("->SIX");
      }
      else if (serialReadInt == 7)
      {
        state = SEVEN;
        lcd.print("->SEVEN");
      }
      else if (serialReadInt == 8)
      {
        state = EIGHT;
        lcd.print("->EIGHT");
      }
      else if (serialReadInt == 9)
      {
        state = NINE;
        lcd.print("->NINE");
      }
      else if (serialReadInt == 10)
      {
        state = TEN;
        lcd.print("->TEN");
      }
      else if (serialReadInt == 11)
      {
        state = ELEVEN;
        lcd.print("->ELEVEN");
      }
      else if (serialReadInt == 12)
      {
        state = TWELVE;
        lcd.print("->TWELVE");
      }
      else if (serialReadInt == 13)
      {
        state = THIRTEEN;
        lcd.print("->THIRTEEN");
      }
      else if (serialReadInt == 14)
      {
        state = FOURTEEN;
        lcd.print("->FOURTEEN");
      }
      else if (serialReadInt == 15)
      {
        state = FIFTEEN;
        lcd.print("->FIFTEEN");
      }
      else if (serialReadInt == 16)
      {
        state = SIXTEEN;
        lcd.print("->SIXTEEN");
      }
      else
      {
        state = ZERO;
      }
      break;

    case ONE:
      digitalWrite(bit0, 1);
      digitalWrite(bit1, 0);
      digitalWrite(bit2, 0);
      digitalWrite(bit3, 0);
      lcd.setCursor(0, 0);
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
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
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
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
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
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
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
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
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
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
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
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
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
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
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
        state = ZERO;
        lcd.clear();
      }
      break;

    case NINE:
      digitalWrite(bit0, 1);
      digitalWrite(bit1, 0);
      digitalWrite(bit2, 0);
      digitalWrite(bit3, 1);
      lcd.setCursor(0, 0);
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
        state = ZERO;
        lcd.clear();
      }
      break;

    case TEN:
      digitalWrite(bit0, 0);
      digitalWrite(bit1, 1);
      digitalWrite(bit2, 0);
      digitalWrite(bit3, 1);
      lcd.setCursor(0, 0);
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
        state = ZERO;
        lcd.clear();
      }
      break;

    case ELEVEN:
      digitalWrite(bit0, 1);
      digitalWrite(bit1, 1);
      digitalWrite(bit2, 0);
      digitalWrite(bit3, 1);
      lcd.setCursor(0, 0);
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
        state = ZERO;
        lcd.clear();
      }
      break;

    case TWELVE:
      digitalWrite(bit0, 0);
      digitalWrite(bit1, 0);
      digitalWrite(bit2, 1);
      digitalWrite(bit3, 1);
      lcd.setCursor(0, 0);
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
        state = ZERO;
        lcd.clear();
      }
      break;

    case THIRTEEN:
      digitalWrite(bit0, 1);
      digitalWrite(bit1, 0);
      digitalWrite(bit2, 1);
      digitalWrite(bit3, 1);
      lcd.setCursor(0, 0);
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
        state = ZERO;
        lcd.clear();
      }
      break;

    case FOURTEEN:
      digitalWrite(bit0, 0);
      digitalWrite(bit1, 1);
      digitalWrite(bit2, 1);
      digitalWrite(bit3, 1);
      lcd.setCursor(0, 0);
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
        state = ZERO;
        lcd.clear();
      }
      break;

    case FIFTEEN:
      digitalWrite(bit0, 1);
      digitalWrite(bit1, 1);
      digitalWrite(bit2, 1);
      digitalWrite(bit3, 1);
      lcd.setCursor(0, 0);
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
        state = ZERO;
        lcd.clear();
      }
      break;

    case SIXTEEN:
      digitalWrite(bit0, 0);
      digitalWrite(bit1, 0);
      digitalWrite(bit2, 0);
      digitalWrite(bit3, 0);
      lcd.setCursor(0, 0);
      lcd.print("Send'$A'to rest");
      if (serialRead() == 17)
      {
        state = ZERO;
        lcd.clear();
      }
      break;
  }
}

int serialRead()
{
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
