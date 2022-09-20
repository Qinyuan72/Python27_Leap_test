//sketch created by Akshay Joseph
#include <Wire.h> 
#include <LiquidCrystal_I2C.h>
#include <stdlib.h>
#include <stdio.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup()
{

  lcd.begin();
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("How are you");
  lcd.setCursor(0,1);
  lcd.print("today?");
}

void loop()
{
  main();
}




enum states {
  START,
  LOOP,
  END,
} state;

enum events {
  START_LOOPING,
  PRINT_HELLO,
  STOP_LOOPING,
};

void step_state(enum events event) {
  switch(state) {
  case START:
    switch(event) {
    case START_LOOPING:
      state = LOOP;
      break;
    default:
      exit(1);
      break;
    }
    break;
  case LOOP:
    switch(event) {
    case PRINT_HELLO:
      printf("Hello World!\n");
      break;
    case STOP_LOOPING:
      state = END;
      break;
    default:
      exit(1);
      break;
    }
    break;
  case END:
    exit(1);
    break;
  }
}

int main(void) {
  step_state(START_LOOPING);
  step_state(PRINT_HELLO);
  step_state(PRINT_HELLO);
  step_state(STOP_LOOPING);
  return 0;
}
