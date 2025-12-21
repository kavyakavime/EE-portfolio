//ESP32 is packet relay
unsigned long packetsReceived = 0;
unsigned long packetsForwarded = 0;

void setup() {
  Serial.begin(115200);  // USB to Raspberry Pi
  Serial1.begin(9600, SERIAL_8N1, 16, 17); // Pin RX = 17, and TX is 18 in ESP32
  Serial.println("ESP32 Relay Active");
  Serial.println("SEQ|NANO_TIME|PAYLOAD|CHECKSUM|ESP_RX_TIME|ESP_TX_TIME");
} //setup

void loop() {
  if (Serial1.available()) {
    unsigned long rxTime = micros(); // Timestamp when received
    String packet = Serial1.readStringUntil('\n');
    packet.trim();
    if (packet.length() > 0) {
      packetsReceived++;
      unsigned long txTime = micros(); // Timestamp before forwarding
      // Forward to Raspberry Pi with added ESP32 timestamps
      Serial.print(packet);
      Serial.print("|");
      Serial.print(rxTime);
      Serial.print("|");
      Serial.println(txTime);
      
      packetsForwarded++;
    } //if
  } //if
  // Report every 5 secs
  static unsigned long lastReport = 0;
  if (millis() - lastReport > 5000) {
    Serial.print("STATUS|RX:");
    Serial.print(packetsReceived);
    Serial.print("|TX:");
    Serial.println(packetsForwarded);
    lastReport = millis();
  } //if
} //lop
