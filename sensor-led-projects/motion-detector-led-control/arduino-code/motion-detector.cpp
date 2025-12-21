// Ultrasonic sensor pins
const int trigPin = 9;
const int echoPin = 10;


// LED pins
int leds[] = {2, 3, 4, 5, 6, 7, 8};
const int numLeds = 7;


// Buzzer pin
const int buzzerPin = 11;


// Distance thresholds (cm)
// cahnge if needed
const int thresholds[] = {
 60, // Green 1
 50, // Green 2
 40, // Yellow 1
 30, // Yellow 2
 20, // Yellow 3 (BUZZER STARTS)
 15, // Red 1
 8   // Red 2 (DANGER)
};


void setup() {
 Serial.begin(115200);


 pinMode(trigPin, OUTPUT);
 pinMode(echoPin, INPUT);
 pinMode(buzzerPin, OUTPUT);


 for (int i = 0; i < numLeds; i++) {
   pinMode(leds[i], OUTPUT);
   digitalWrite(leds[i], LOW);
 }


 digitalWrite(buzzerPin, LOW);
}


long getDistanceCM() { //make distance to cm
 digitalWrite(trigPin, LOW);
 delayMicroseconds(2);


 digitalWrite(trigPin, HIGH);
 delayMicroseconds(10);
 digitalWrite(trigPin, LOW);


 long duration = pulseIn(echoPin, HIGH, 30000); 
 if (duration == 0) return 999; 


 long distance = duration * 0.034 / 2;
 return distance;
}


void loop() {
 long distance = 0;
 for (int i = 0; i < 3; i++) {
   distance += getDistanceCM();
   delay(10);
 }
 distance /= 3;


 Serial.print("Distance: ");
 Serial.print(distance);
 Serial.println(" cm");


 // Turn off everything first
 for (int i = 0; i < numLeds; i++) {
   digitalWrite(leds[i], LOW);
 }
 digitalWrite(buzzerPin, LOW);


 // Turn on LEDs based on distance
 for (int i = 0; i < numLeds; i++) {
   if (distance <= thresholds[i]) {
     digitalWrite(leds[i], HIGH);
   }
 }


 // Buzzer logic (starts at 3rd yellow LED)
 if (distance <= thresholds[4]) {
   digitalWrite(buzzerPin, HIGH);
 }


 delay(50); // delay
}
