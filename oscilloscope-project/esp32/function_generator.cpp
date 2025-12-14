#include <Arduino.h>
#include <math.h>

const int dacPin = 25;         // ESP32 DAC output pin
const int tableSize = 256;     // 256 points for sin table
uint8_t sineTable[tableSize];  

// List of frequencies for testing / sweep (Hz)
float freq_list[] = {100, 200, 500, 1000, 2000, 5000};
int numFreqs = sizeof(freq_list)/sizeof(freq_list[0]);

void setup() {
  // Precompute sine table (0–255 DAC)
  for (int i = 0; i < tableSize; i++) {
    sineTable[i] = 127 + 127 * sin(2 * PI * i / tableSize);
  }

  Serial.begin(115200); // optional: debug
  Serial.println("ESP32 DAC Function Generator Started");
}


void loop() {
  // Loop through frequency list
  for (int fIdx = 0; fIdx < numFreqs; fIdx++) {
    float freq = freq_list[fIdx];
    
    // Compute delay per DAC update to achieve desired frequency
    float delayMicroSec = 1000000.0 / (freq * tableSize); // period over tableSize

    Serial.print("Frequency: ");
    Serial.print(freq);
    Serial.println(" Hz");

    // Generate waveform for  approx 0.5 seconds per frequency
    unsigned long startTime = millis();
    while (millis() - startTime < 500) { // 0.5 sec
      for (int i = 0; i < tableSize; i++) {
        dacWrite(dacPin, sineTable[i]);
        delayMicroseconds(delayMicroSec);
      }
    }
  }

  // Stop after one sweep
  while(1); 
}
