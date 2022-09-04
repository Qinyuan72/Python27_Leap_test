#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <ESP8266WiFi.h>

const char* ssid     = "NETGEAR_THE_GREAT";
const char* password = "MyGreatNetwork";
WiFiServer wifiServer(8080);
LiquidCrystal_I2C lcd(0x27, 16, 2);
  
void setup() 
{
    Serial.begin(115200);
    Wire.begin(D1, D2);
    lcd.begin();
    lcd.clear();
    lcd.print("LCD,Initalized.");
 
    Serial.println("Serial_set_up_success");


    WiFi.begin(ssid, password);
    lcd.clear();
    lcd.print("Wi-Fi connecting                       ");
    while (WiFi.status() != WL_CONNECTED)
     {
        delay(500);
        lcd.print(".");
        Serial.print(".");
     }
    Serial.println("WiFi connected.");
    lcd.clear();
    lcd.print("Wi-Fi connected                         ");
    lcd.print("IP");
    lcd.print(WiFi.localIP());
    wifiServer.begin();
}

void loop()
{
  WiFiClient client = wifiServer.available();
  if (client) {
    while (client.connected()) {
      while (client.available()>0) {
        char c = client.read();
        if (c == '$'){
           lcd.clear();
           lcd.setCursor(0,0);
        }
        else;
        {
          //Serial.println(c);
          lcd.print(c);
        }
    }}
    client.stop();
    Serial.println("Client disconnected");
    lcd.clear();
    lcd.print("Client                                  disconnected");
   }
 }