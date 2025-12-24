//Arduino nano sends random, but structured messages to ESP 32 #1
unsigned long messageCount = 0;
unsigned long lastSendTime = 0;
const unsigned long SEND_INTERVAL = 2000; // every two seconds, send packet


void setup() {
 Serial.begin(9600);
 randomSeed(analogRead(A0));
}


void loop() {
  unsigned long currentTime = millis();
  if (currentTime - lastSendTime >= SEND_INTERVAL) {
   // Generate message in this structure: COUNT|TIMESTAMP|DATA
  String message = String(messageCount) + "|" +
                    String(currentTime) + "|" +
                    generateRandomData();
  
   Serial.println(message);
  
   messageCount++;
   lastSendTime = currentTime;
 } //if
} //loop


String generateRandomData() {
 // Random 4-character string
 String data = "";
 for (int i = 0; i < 4; i++) {
   data += char(random(65, 91)); // A-Z
 }
 return data;
} //generateRandomData
