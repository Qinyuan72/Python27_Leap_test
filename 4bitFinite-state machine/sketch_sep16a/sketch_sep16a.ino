//sketch created by Akshay Joseph
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup()
{

  lcd.begin();


  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Hello World!");
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

int main(void) {
  step_state(START_LOOPING);
  delay(1000);
  step_state(PRINT_HELLO);
  delay(1000);
  step_state(PRINT_HELLO);
  delay(1000);
  step_state(STOP_LOOPING);
  return 0;
}
void step_state(enum events event) {
  switch (state) {
    case START:
      switch (event) {
        case START_LOOPING:
          state = LOOP;
          break;
        default:
          exit(1);
          break;
      }
      break;
    case LOOP:
      switch (event) {
        case PRINT_HELLO:
          //printf("Hello World!\n");
          lcd.clear();
          lcd.setCursor(0, 0);
          lcd.print("Hello World!");
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
