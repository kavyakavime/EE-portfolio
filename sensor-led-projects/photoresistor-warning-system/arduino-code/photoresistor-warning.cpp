const int ldrPin = A0;
const int buzzerPin = 12;


// LED pins (2 green, 3 yellow, 2 red)
int leds[] = {2, 3, 4, 5, 6, 7, 8};
const int numLeds = 7;

int thresholds[] = {
 450, // Green 1
 400, // Green 2
 350, // Yellow 1
 300, // Yellow 2
 250, // Yellow 3 (buzzer begins)
 200, // Red 1
 150  // Red 2 (darrk)
};


void setup() {
 Serial.begin(9600);


 pinMode(buzzerPin, OUTPUT);
 digitalWrite(buzzerPin, LOW);


 for (int i = 0; i < numLeds; i++) {
   pinMode(leds[i], OUTPUT);
   digitalWrite(leds[i], LOW);
 }


 Serial.println("Analog Light Warning System Ready");
}


void loop() {
 int light = 0;
 for (int i = 0; i < 5; i++) {
   light += analogRead(ldrPin);
   delay(5);
 }
 light /= 5;


 Serial.print("Light level: ");
 Serial.println(light);


 // Turn everything OFF first
 for (int i = 0; i < numLeds; i++) {
   digitalWrite(leds[i], LOW);
 }
 digitalWrite(buzzerPin, LOW);


 // LEDs turn ON as it gets darker
 for (int i = 0; i < numLeds; i++) {
   if (light <= thresholds[i]) {
     digitalWrite(leds[i], HIGH);
   }
 }


 // Buzzer activates when light is very dark
 if (light <= 200) {
   digitalWrite(buzzerPin, HIGH);
 }


 delay(100);
}
