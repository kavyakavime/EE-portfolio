// sends packets to ESP32
unsigned long packetCount = 0;
const unsigned long PACKET_INTERVAL = 100; // Send every (10 packets/sec)
unsigned long lastSendTime = 0;

void setup() {
  Serial.begin(9600);
  randomSeed(analogRead(A0)); //random
}

void loop() {
  unsigned long currentTime = millis();
  
  if (currentTime - lastSendTime >= PACKET_INTERVAL) {
    // packet generating like: SEQ|TIMESTAMP|PAYLOAD|CHECKSUM
    String payload = generatePayload();
    unsigned int checksum = calculateChecksum(payload);
    
    String packet = String(packetCount) + "|" + 
                    String(currentTime) + "|" + 
                    payload + "|" + 
                    String(checksum);
    
    Serial.println(packet);
    
    packetCount++;
    lastSendTime = currentTime;
  }
}

String generatePayload() {
  // Random 8-character payload 
  String payload = "";
  for (int i = 0; i < 8; i++) {
    payload += char(random(65, 91)); 
  }
  return payload;
}

unsigned int calculateChecksum(String data) {
  // checksome of all the ASCII characters
  unsigned int sum = 0;
  for (unsigned int i = 0; i < data.length(); i++) {
    sum += data[i];
  }
  return sum % 65536;
}
