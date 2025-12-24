
// This is the ESP number two that acts like a receiver, 
// displays data in the LCD, and converts serial to pi. 

#include <esp_now.h>
#include <WiFi.h>
#include <esp_wifi.h>
#include <LiquidCrystal.h>

#define ESPNOW_CHANNEL 1   
#define LCD_COLS 16 
#define LCD_ROWS 2

// LCD pins (RS, E, D4, D5, D6, D7) - adjust for ypurs
LiquidCrystal lcd(5, 18, 23, 22, 21, 19);

typedef struct {
  char message[64];
  unsigned long esp1_timestamp;
} WirelessPacket;

volatile bool gotPacket = false;   // flag for loop()
WirelessPacket lastPacket;
unsigned long packetsReceived = 0;
unsigned long lastLatencyMs = 0;


void onDataRecv(const esp_now_recv_info *recv_info, const uint8_t *data, int len) {
  if (len < (int)sizeof(WirelessPacket)) {
    return;
  }

  memcpy((void*)&lastPacket, data, sizeof(WirelessPacket));
  lastLatencyMs = millis() - lastPacket.esp1_timestamp;
  packetsReceived++;
  gotPacket = true;

  // printing who sent it
  Serial.print("RX from ");
  for (int i = 0; i < 6; i++) {
    Serial.printf("%02X", recv_info->src_addr[i]);
    if (i < 5) Serial.print(":");
  }
  Serial.println();
}

void showBootScreen() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("ESP32 Receiver");
  lcd.setCursor(0, 1);
  lcd.print("Waiting...");
}

void setup() {
  Serial.begin(115200);
  delay(300);

  // startig LCD
  lcd.begin(LCD_COLS, LCD_ROWS);
  showBootScreen();

  // important for initializing wifi
  WiFi.mode(WIFI_STA);

  //force wifi channel
  esp_wifi_set_channel(ESPNOW_CHANNEL, WIFI_SECOND_CHAN_NONE);

  Serial.println("\n=== ESP32 #2 - ESP-NOW Receiver + LCD ===");
  Serial.print("MAC Address: ");
  Serial.println(WiFi.macAddress());
  Serial.print("Channel forced to: ");
  Serial.println(ESPNOW_CHANNEL);

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed!");
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("ESP-NOW FAIL");
    lcd.setCursor(0, 1);
    lcd.print("Check wiring");
    while (1) delay(1000);
  }

  esp_now_register_recv_cb(onDataRecv);

  Serial.println("Ready to receive packets.\n");
}

void loop() {
  if (gotPacket) {
    gotPacket = false;

    // 
    lcd.clear();

    // Line 1: RX count + latency
    lcd.setCursor(0, 0);
    lcd.print("RX:");
    lcd.print(packetsReceived);
    lcd.print(" L:");
    lcd.print(lastLatencyMs);
    lcd.print("ms");

    // Line 2: first 16 chars of message cuz its small LCD -adjust if needed
    lcd.setCursor(0, 1);
    char line2[LCD_COLS + 1];
    strncpy(line2, lastPacket.message, LCD_COLS);
    line2[LCD_COLS] = '\0';
    lcd.print(line2);

    // send info to rasberry pi
    Serial.print("PACKET|");
    Serial.print(lastPacket.message);
    Serial.print("|LATENCY:");
    Serial.print(lastLatencyMs);
    Serial.print("|COUNT:");
    Serial.println(packetsReceived);
  }

  delay(10); //delay for smoothness
}
