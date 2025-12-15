#include <Arduino.h>
#include <math.h>



static const int DAC_PIN = 25;
static const int TABLE_SIZE = 256;
uint8_t sineTable[TABLE_SIZE];

float freqHz = 5000.0;   // Hz

void setup() {
  Serial.begin(115200);

  // Build sine lookup table (0–255 - 0–3.3V)
  for (int i = 0; i < TABLE_SIZE; i++) {
    float s = sinf(2.0f * PI * i / TABLE_SIZE);
    int v = (int)(127.5f + 127.0f * s);
    if (v < 0) v = 0;
    if (v > 255) v = 255;
    sineTable[i] = (uint8_t)v;
  }

  Serial.println("ESP32 DAC Function Generator Ready");
  Serial.print("Frequency = ");
  Serial.print(freqHz);
  Serial.println(" Hz");
}

void loop() {
  // Period per sample
  float samplePeriodUs = 1000000.0 / (freqHz * TABLE_SIZE);

  for (int i = 0; i < TABLE_SIZE; i++) {
    dacWrite(DAC_PIN, sineTable[i]);
    delayMicroseconds((uint32_t)samplePeriodUs);
  }
}

