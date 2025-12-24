// =====================================
// ESP32 #1 - UART to Wireless Bridge
// Receives from Nano, sends wirelessly
// =====================================




#include <esp_now.h>
#include <WiFi.h>
#include <esp_wifi.h>  // Add this line






#define LED_PIN 2  // Built-in LED




// ESP32 #2 MAC Address (GET THIS IN STEP 3)
uint8_t receiverMAC[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};


typedef struct {
char message[64];
unsigned long esp1_timestamp;
} WirelessPacket;




WirelessPacket outPacket;
unsigned long packetsForwarded = 0;




void onDataSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {
if (status == ESP_NOW_SEND_SUCCESS) {
  digitalWrite(LED_PIN, HIGH);
  delay(50);
  digitalWrite(LED_PIN, LOW);
}
}




void setup() {
Serial.begin(115200);  // USB debug
Serial1.begin(9600, SERIAL_8N1, 16, 17); // UART from Nano (RX=16, TX=17)
 pinMode(LED_PIN, OUTPUT);
 WiFi.mode(WIFI_STA);
 esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
 Serial.println("\n=== ESP32 #1 - Wireless Transmitter ===");
Serial.print("MAC Address: ");
Serial.println(WiFi.macAddress());
Serial.println("Waiting for Nano data...\n");
 if (esp_now_init() != ESP_OK) {
  Serial.println("ESP-NOW init failed!");
  return;
}
 esp_now_register_send_cb(onDataSent);
 // Add ESP32 #2 as peer
esp_now_peer_info_t peerInfo = {};
memcpy(peerInfo.peer_addr, receiverMAC, 6);
peerInfo.channel = 1;   // MUST MATCH
peerInfo.encrypt = false;


if (esp_now_add_peer(&peerInfo) != ESP_OK) {
 Serial.println("Failed to add peer!");
} //if
}




void loop() {
// Read from Nano via UART
if (Serial1.available()) {
  String nanoMessage = Serial1.readStringUntil('\n');
  nanoMessage.trim();
   if (nanoMessage.length() > 0) {
    // Prepare wireless packet
    nanoMessage.toCharArray(outPacket.message, 64);
    outPacket.esp1_timestamp = millis();
  
    // Send wirelessly to ESP32 #2
    esp_err_t result = esp_now_send(receiverMAC, (uint8_t *)&outPacket, sizeof(outPacket));
  
    packetsForwarded++;
  
    Serial.print("[TX] ");
    Serial.print(nanoMessage);
    Serial.print(" | Forwarded: ");
    Serial.println(packetsForwarded);
  }
}
}
