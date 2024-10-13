#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <ArduinoJson.h>  // Include ArduinoJson library

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET -1
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define STASSID "Xiaomi_3D3E"
#define STAPSK  "2019newpassword"
WiFiServer wifiServer(8080);

void setup() {
  Serial.begin(115200);
  Wire.begin(5, 4);

  // Initialize the OLED display
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("Connecting to WiFi");
  display.display();

  // Connect to Wi-Fi
  WiFi.begin(STASSID, STAPSK);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    display.print(".");
    display.display();
  }

  display.clearDisplay();
  display.println("Wi-Fi connected");
  display.print("IP: ");
  display.println(WiFi.localIP());
  wifiServer.begin();
  display.display();
}

void displayData(float cpu, float ram, float temp, float network) {
  // Display parsed data on the OLED screen
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
    String jsonString = "";  // Raw JSON string
    Serial.println("Waiting for client data...");
    
    while (client.connected()) {
      while (client.available() > 0) {
        char c = client.read();
        jsonString += c;

        // If the end of the JSON object is reached
        if (c == '}') {
          // Print the raw received JSON string
          Serial.println("Received full message:");
          Serial.println(jsonString);

          // Parse the JSON string
          StaticJsonDocument<200> doc;
          DeserializationError error = deserializeJson(doc, jsonString);
          
          // Check if parsing was successful
          if (error) {
            Serial.print("JSON Deserialization failed: ");
            Serial.println(error.c_str());
          } else {
            // Extract values from the JSON
            float cpu = doc["cpu"];
            float ram = doc["ram"];
            float temp = doc["temp"];
            float network = doc["network"];

            // Print parsed values for debugging
            Serial.println("Parsed values:");
            Serial.print("Parsed CPU: ");
            Serial.println(cpu);
            Serial.print("Parsed RAM: ");
            Serial.println(ram);
            Serial.print("Parsed TEMP: ");
            Serial.println(temp);
            Serial.print("Parsed NET: ");
            Serial.println(network);

            // Display the parsed data on the OLED
            displayData(cpu, ram, temp, network);
          }

          // Clear the string for the next JSON message
          jsonString = "";
        }
      }
    }

    client.stop();
    Serial.println("Client disconnected");
  }
}
