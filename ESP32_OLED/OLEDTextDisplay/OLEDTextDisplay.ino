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

#define STASSID "Xiaomi_3D3E"       // Wi-Fi SSID
#define STAPSK  "2019newpassword"   // Wi-Fi password
WiFiServer wifiServer(8080);        // Start Wi-Fi server on port 8080

void setup() {
  Serial.begin(115200);
  Serial.println("Serial setup successful");
  
  // Start I2C on specific pins
  Wire.begin(5, 4);
  
  // Initialize the OLED display
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for (;;); // Don't proceed, loop forever
  }
  display.display();
  delay(500);
  display.clearDisplay();
  display.setTextSize(1);      // Normal 1:1 pixel scale
  display.setTextColor(WHITE); // Draw white text
  display.setCursor(0, 0);     // Start at top-left corner
  display.println("Wifi connecting");
  display.display();

  // Connect to Wi-Fi
  WiFi.begin(STASSID, STAPSK);
  display.clearDisplay();
  display.setTextSize(1);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    display.print(".");
    Serial.print(".");
    display.display();
  }

  // Once connected, display IP address
  Serial.println("\nWiFi connected.");
  display.println("Wi-Fi connected");
  display.print("IP: ");
  display.println(WiFi.localIP());
  wifiServer.begin();           // Start the server
  display.display();
}

void loop() {
  char buffer[120];             // Increased buffer size to handle more data
  int i = 0;
  bool displayPrint = false;     // Track when to update the display
  WiFiClient client = wifiServer.available(); // Check for new client
  
  if (client) {
    while (client.connected()) {
      while (client.available() > 0) {
        char c = client.read();
        
        // Reset buffer if start of new message ('$' is the delimiter)
        if (c == '$') {
          i = 0;
          memset(buffer, 0, sizeof(buffer)); // Clear buffer
          display.setCursor(0, 0);
          display.clearDisplay();
        } else {
          // Add character to buffer until buffer is full or message is complete
          if (i < sizeof(buffer) - 1) {
            buffer[i++] = c;
            buffer[i] = '\0';  // Null-terminate the string
            displayPrint = true; // Set flag to print updated buffer
          }
        }
      }

      // Only update display if new data has been processed
      if (displayPrint) {
        Serial.println(buffer);   // Print to Serial Monitor
        display.clearDisplay();   // Clear previous display
        display.setCursor(0, 0);  // Reset cursor position
        display.print(buffer);    // Print buffer content on OLED
        display.display();        // Update OLED
        displayPrint = false;     // Reset flag after displaying
      }
    }

    // Stop client and notify when disconnected
    client.stop();
    Serial.println("Client disconnected");
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Client disconnected");
    display.display();
  }
}
