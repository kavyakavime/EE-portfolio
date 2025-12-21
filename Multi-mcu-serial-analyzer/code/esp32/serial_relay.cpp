// ========================================
// ESP32 - Packet Relay with Latency Measurement
// Receives from Nano, adds timestamp, sends to Pi
// ========================================

unsigned long packetsReceived = 0;
unsigned long packetsForwarded = 0;

void setup() {
  Serial.begin(115200);  // USB to Raspberry Pi
  Serial1.begin(9600, SERIAL_8N1, 16, 17); // UART from Nano (RX=16, TX=17)
  
  Serial.println("ESP32 Relay Active");
  Serial.println("SEQ|NANO_TIME|PAYLOAD|CHECKSUM|ESP_RX_TIME|ESP_TX_TIME");
}

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
    }
  }
  
  // Optional: Status report every 5 seconds
  static unsigned long lastReport = 0;
  if (millis() - lastReport > 5000) {
    Serial.print("STATUS|RX:");
    Serial.print(packetsReceived);
    Serial.print("|TX:");
    Serial.println(packetsForwarded);
    lastReport = millis();
  }
}
