const int potPin = A0;
const int buzzerPin = 12;


// LED pins (2 green, 3 yellow, 2 red)
int leds[] = {2, 3, 4, 5, 6, 7, 8};
const int numLeds = 7;


void setup() {
 Serial.begin(9600);


 pinMode(buzzerPin, OUTPUT);
 digitalWrite(buzzerPin, LOW);


 for (int i = 0; i < numLeds; i++) {
   pinMode(leds[i], OUTPUT);
   digitalWrite(leds[i], LOW);
 }


 Serial.println("Potentiometer Warning System Ready");
}


void loop() {
 int potValue = analogRead(potPin);  // 0–1023


 Serial.print("Pot value: ");
 Serial.println(potValue);


 // Map pot value to number of LEDs
 int level = map(potValue, 0, 1023, 0, numLeds);
 level = constrain(level, 0, numLeds);


 // Update LEDs
 for (int i = 0; i < numLeds; i++) {
   digitalWrite(leds[i], i < level ? HIGH : LOW);
 }


 // thrid yellow light that buzzer turns off
 if (level >= 5) {
   digitalWrite(buzzerPin, HIGH);
 } else {
   digitalWrite(buzzerPin, LOW);
 }


 delay(50);
}

