

const uint16_t FS_HZ = 2000; // (2k frames/sec)
const uint8_t VIN_CH = 0;    // A0
const uint8_t VOUT_CH = 1;   // A1

static inline void sendFrame(uint16_t vin, uint16_t vout) {
  Serial.write(0xAA);
  Serial.write(0x55);
  Serial.write((uint8_t)(vin & 0xFF));
  Serial.write((uint8_t)((vin >> 8) & 0xFF));
  Serial.write((uint8_t)(vout & 0xFF));
  Serial.write((uint8_t)((vout >> 8) & 0xFF));
}

void setup() {
  Serial.begin(230400); // faster than 115200 for binary streaming
}

void loop() {
  static uint32_t nextMicros = micros();
  const uint32_t period = 1000000UL / FS_HZ;

  // Wait until next sample time
  while ((int32_t)(micros() - nextMicros) < 0) { /* tight wait */ }
  nextMicros += period;

  // Read channels
  uint16_t vin  = analogRead(VIN_CH);   // A0
  uint16_t vout = analogRead(VOUT_CH);  // A1

  sendFrame(vin, vout);
}

