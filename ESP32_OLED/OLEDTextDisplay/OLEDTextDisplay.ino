
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define STASSID "Xiaomi_3D3E"
#define STAPSK  "2019newpassword"
WiFiServer wifiServer(8080);

void setup()
{

  Serial.begin(115200);
  Serial.println("Serial setup successful");
  Wire.begin(5, 4);
  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
  {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;)
      ; // Don't proceed, loop forever
  }
  display.display();
  delay(500);
  display.clearDisplay();
  display.setTextSize(1);      // Normal 1:1 pixel scale
  display.setTextColor(WHITE); // Draw white text
  display.setCursor(0, 0);     // Start at top-left corner
  display.println("Wifi connecting");

  WiFi.begin(STASSID, STAPSK);

  display.clearDisplay();
  display.setTextSize(1);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    display.print(".");
    Serial.print(".");
    display.display();
  }
  Serial.println("WiFi connected.");
  display.println("Wi-Fi connected");
  display.print("IP: ");
  display.print(WiFi.localIP());
  wifiServer.begin();
  display.display();
}

void loop()
{
  char buffer[60];
  int i = 0;
  bool dispalyPrint = 1;
  WiFiClient client = wifiServer.available();
  display.display();

  if (client) {
    while (client.connected()) {
      while (client.available() > 0) {
        char c = client.read();
        if (c == '$') {
          i = 0;
          display.setCursor(0, 0);
          display.clearDisplay();
        }
        else;
        {
          buffer[i++] = c;
        }
        buffer[i] = '\0';
        dispalyPrint = 1;
      }
      if (dispalyPrint) {
        Serial.println(buffer);
        display.print(buffer);
        display.display();
        dispalyPrint = 0;
      }
    }
    client.stop();
    Serial.println("Client disconnected");
    display.println("\nClient disconnected");
    display.display();
  }
}
