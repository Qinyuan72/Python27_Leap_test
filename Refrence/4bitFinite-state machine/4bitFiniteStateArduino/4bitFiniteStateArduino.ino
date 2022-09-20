int setPin;
void setup()
{
  Serial.begin(115200);
  Serial.println("Serial_set_up_success");
  pinMode(1, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  pinMode(9, OUTPUT);
}

void loop()
{
  while (Serial.available() > 0)
  {
    char c = Serial.read();
    if (c == '$')
    {
      Serial.println("'$'Received");
      char c = Serial.read();
      setPin = c - 48;
      digitalWrite(setPin, LOW);
      Serial.println(setPin);
    }
    if (c == '^')
    {
      Serial.println("'^'Received");
      char c = Serial.read();
      setPin = c - 48;
      digitalWrite(setPin, HIGH);
      Serial.println(setPin);
    }
    else
    {
      Serial.print(c);
    }
  }
}
