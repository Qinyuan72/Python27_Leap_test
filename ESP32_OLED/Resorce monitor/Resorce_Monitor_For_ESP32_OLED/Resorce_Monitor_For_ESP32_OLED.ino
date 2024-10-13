#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <WiFi.h>
#include <ArduinoJson.h>
#include "esp_timer.h"  // ESP32 timer library

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels

#define OLED_RESET -1 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define STASSID "Xiaomi_3D3E"       // Wi-Fi SSID
#define STAPSK  "2019newpassword"   // Wi-Fi password
WiFiServer wifiServer(8080);        // Start Wi-Fi server on port 8080

// Custom arrows for up and down
const uint8_t upArrow[] PROGMEM = {
  0x08, 0x1C, 0x3E, 0x7F, 0x08, 0x08, 0x08, 0x08
};
const uint8_t downArrow[] PROGMEM = {
  0x08, 0x08, 0x08, 0x08, 0x7F, 0x3E, 0x1C, 0x08
};

// Variables for flickering arrows
volatile bool showUpArrow = true;
volatile bool showDownArrow = true;

// Timer handles
esp_timer_handle_t flickerTimerHandle;
esp_timer_handle_t screenSaverTimerHandle;

// ISR Timer callback for flickering
void IRAM_ATTR onFlickerTimer(void* arg) {
    showUpArrow = !showUpArrow;
    showDownArrow = !showDownArrow;
}

// ISR Timer callback for screen saver (OLED off)
void IRAM_ATTR onScreenSaverTimeout(void* arg) {
    // Check if the client is disconnected
    WiFiClient client = wifiServer.available();
    if (!client) {
        // Clear the OLED display if no client is connected
        display.clearDisplay();
        display.display();
        Serial.println("Client disconnected, OLED cleared.");
    }
}

// Set up flicker timer for arrows
void setupFlickerTimer() {
    esp_timer_create_args_t timerArgs = {
        .callback = &onFlickerTimer,  // Timer ISR function
        .name = "arrow_flicker"
    };
    esp_timer_create(&timerArgs, &flickerTimerHandle);
    esp_timer_start_periodic(flickerTimerHandle, 10000);  // 100ms interval
}

// Set up screen saver timer to check connection after 20 seconds
void setupScreenSaverTimer() {
    esp_timer_create_args_t timerArgs = {
        .callback = &onScreenSaverTimeout,  // Timer ISR function
        .name = "screen_saver_timeout"
    };
    esp_timer_create(&timerArgs, &screenSaverTimerHandle);
    esp_timer_start_periodic(screenSaverTimerHandle, 20000000);  // 20 seconds interval
}

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

  // Set up ISR Timers
  setupFlickerTimer();
  setupScreenSaverTimer();
}

// Function to convert network speed to proper unit with no decimal for Kbps and bps, and proper formatting for Mbps
void formatNetworkSpeed(float speed, char *buffer, int bufferSize) {
    if (speed < 3000) {  // Less than 3 Kbps = bps
        snprintf(buffer, bufferSize, "%.0f bps", speed);
    } else if (speed < 50 * 1000) {  // Less than 50 Kbps = Kbps
        snprintf(buffer, bufferSize, "%.0f Kbps", speed / 1000);
    } else {  // 50 Kbps and above = Mbps
        snprintf(buffer, bufferSize, "%.2f Mbps", speed / (1000 * 1000));
    }
}

// Function to draw a percentage-based bar (for CPU and RAM)
void drawProgressBar(int x, int y, int width, int height, float percentage) {
  int filledWidth = (int)(width * (percentage / 100.0));
  display.drawRect(x, y, width, height, WHITE); // Draw border
  display.fillRect(x, y, filledWidth, height, WHITE); // Fill according to percentage
}

// Function to display the CPU, RAM, and network speed
void displayData(float cpu, float ram, float upSpeed, float downSpeed) {
  display.clearDisplay();
  
  // RAM at the top
  display.setCursor(0, 0);
  display.printf("RAM: %.1f%%", ram);
  drawProgressBar(65, 0, 60, 8, ram);  // RAM bar with spacing for text
  
  // CPU below RAM
  display.setCursor(0, 16);
  display.printf("CPU: %.1f%%", cpu);
  drawProgressBar(65, 16, 60, 8, cpu);  // CPU bar
  
  // Network Upload Speed with toggling arrow
  char upBuffer[20], downBuffer[20];
  formatNetworkSpeed(upSpeed, upBuffer, sizeof(upBuffer));
  display.setCursor(0, 32);
  
  if (upSpeed > 5 * 1000 * 1000) {  // Toggle arrow only for speeds > 5Mbps
    if (showUpArrow) {
      display.drawBitmap(0, 32, upArrow, 8, 8, WHITE);  // Draw upload arrow
    }
  } else {
    display.drawBitmap(0, 32, upArrow, 8, 8, WHITE);  // Static arrow for low speeds
  }
  display.setCursor(12, 32);
  display.printf("Up: %s", upBuffer);
  
  // Network Download Speed with toggling arrow
  formatNetworkSpeed(downSpeed, downBuffer, sizeof(downBuffer));
  display.setCursor(0, 48);
  
  if (downSpeed > 5 * 1000 * 1000) {  // Toggle arrow only for speeds > 5Mbps
    if (showDownArrow) {
      display.drawBitmap(0, 48, downArrow, 8, 8, WHITE);  // Draw download arrow
    }
  } else {
    display.drawBitmap(0, 48, downArrow, 8, 8, WHITE);  // Static arrow for low speeds
  }
  display.setCursor(12, 48);
  display.printf("Down: %s", downBuffer);

  display.display();
}

void loop() {
  // Handle incoming data
  WiFiClient client = wifiServer.available();
  if (client) {
    String jsonString = "";
    while (client.connected()) {
      while (client.available() > 0) {
        char c = client.read();
        jsonString += c;

        if (c == '}') {  // End of JSON message
          Serial.print("Received full message:\n");
          Serial.println(jsonString);  // Print the raw JSON received

          // Remove any extra characters before the JSON data
          jsonString.trim();

          // Clean up JSON string, removing any unexpected characters like `$`
          int startIndex = jsonString.indexOf('{');
          if (startIndex != -1) {
            jsonString = jsonString.substring(startIndex);  // Start at the first '{'
          }

          StaticJsonDocument<200> doc;
          DeserializationError error = deserializeJson(doc, jsonString);

          if (error) {
            Serial.print("JSON Deserialization failed: ");
            Serial.println(error.c_str());
          } else {
            // Extracting data from JSON
            float cpu = doc["cpu"];
            float ram = doc["ram"];
            float upSpeed = doc["up_speed"];
            float downSpeed = doc["down_speed"];

            // Debug print parsed values
            Serial.printf("Parsed CPU: %.2f\n", cpu);
            Serial.printf("Parsed RAM: %.2f\n", ram);
            Serial.printf("Parsed UPLOAD: %.2f\n", upSpeed);
            Serial.printf("Parsed DOWNLOAD: %.2f\n", downSpeed);
            Serial.println();

            // Display data on OLED
            displayData(cpu, ram, upSpeed, downSpeed);
          }

          jsonString = "";  // Clear the string for the next JSON
        }
      }
    }
    client.stop();
    Serial.println("Client disconnected");

    // After the client is disconnected, we trigger a display clearing message.
    display.clearDisplay();
    display.setCursor(0, 0);
    display.setTextSize(1);
    display.setTextColor(WHITE);
    display.println("Client Disconnected");
    display.display();
    
    // Wait for 5 seconds before clearing the OLED to save power
    delay(5000);  
    display.println("Restarting system...");
    Serial.println("Restarting system...");
    display.display();
    delay(5000);
    esp_restart();
  }
}


