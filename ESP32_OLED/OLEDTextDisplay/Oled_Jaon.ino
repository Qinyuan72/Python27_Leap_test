#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <ArduinoJson.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define STASSID "Xiaomi_3D3E"       // Wi-Fi SSID
#define STAPSK  "2019newpassword"   // Wi-Fi password
WiFiServer wifiServer(8080);        // Start Wi-Fi server on port 8080

void setup() {
  Serial.begin(115200);
  Serial.println("Serial setup successful");

  Wire.begin(5, 4);

  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }
  display.display();
  delay(500);
  display.clearDisplay();

  display.setTextSize(1);      
  display.setTextColor(WHITE); 
  display.setCursor(0, 0);     
  display.println("Connecting to WiFi");
  display.display();

  WiFi.begin(STASSID, STAPSK);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    display.print(".");
    Serial.print(".");
    display.display();
  }

  Serial.println("\nWiFi connected.");
  display.clearDisplay();
  display.println("Wi-Fi connected");
  display.print("IP: ");
  display.println(WiFi.localIP());
  wifiServer.begin();
  display.display();
}

void displayData(float cpu, float ram, float temp, float network) {
  display.clearDisplay();
  display.setCursor(0, 0);
  display.printf("CPU: %.1f%%\n", cpu);
  display.printf("RAM: %.1f%%\n", ram);
  display.printf("TEMP: %.1fC\n", temp);
  display.printf("NET: %.1f Kbps\n", network);
  display.display();
}

void loop() {
  WiFiClient client = wifiServer.available();
  if (client) {
    String jsonString = "";
    while (client.connected()) {
      while (client.available() > 0) {
        char c = client.read();
        jsonString += c;
        if (c == '}') {
          StaticJsonDocument<200> doc;
          deserializeJson(doc, jsonString);

          float cpu = doc["cpu"];
          float ram = doc["ram"];
          float temp = doc["temp"];
          float network = doc["network"];

          displayData(cpu, ram, temp, network);

          jsonString = "";  // Clear the string for the next JSON
        }
      }
    }
    client.stop();
    Serial.println("Client disconnected");
  }
}
