const int inputPin = A1;
const int outputPin = A0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int vin = analogRead(inputPin);
  int vout = analogRead(outputPin);

  Serial.print(vin); 
  Serial.print(",");
  Serial.println(vout);

  delayMicroseconds(500);
}
