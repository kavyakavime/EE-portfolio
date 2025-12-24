//ESP 32 number one that gets data from arduino nano 
// and forwards it to the ESP number 2 through wifi.

#include <esp_now.h>
#include <WiFi.h>
#include <esp_wifi.h>  

#define LED_PIN 2  // Built-in LED

//very important(causes debugging ussues). Update your ESP32 number 2's 
// mac address here. Or eles, packets cannot be sent.
uint8_t receiverMAC[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

typedef struct {
char message[64];
unsigned long esp1_timestamp;
} WirelessPacket;

WirelessPacket outPacket;
unsigned long packetsForwarded = 0;

//make blue build in led blisnk when data is sent.
void onDataSent(const wifi_tx_info_t *info, esp_now_send_status_t status) {
  if (status == ESP_NOW_SEND_SUCCESS) {
    digitalWrite(LED_PIN, HIGH);
    delay(50);
    digitalWrite(LED_PIN, LOW);
  }
} //onDataSent

void setup() {
  Serial.begin(115200);  // USB debug
  Serial1.begin(9600, SERIAL_8N1, 16, 17); // UART from Nano 
  pinMode(LED_PIN, OUTPUT);
  WiFi.mode(WIFI_STA);
  esp_wifi_set_channel(1, WIFI_SECOND_CHAN_NONE);
  Serial.println("\nESP32 #1 - Wireless Transmitter"); //for your use
  Serial.print("MAC Address: ");
  Serial.println(WiFi.macAddress());
  Serial.println("Waiting for Nano data...\n");
  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed!");
    return;
  } //if
  esp_now_register_send_cb(onDataSent);
  // Add ESP32 #2 as peer
  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, receiverMAC, 6);
  peerInfo.channel = 1;   
  peerInfo.encrypt = false;
  
  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer!");
  } //if
} //setup




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
    } //if
  } //if
} //loop
