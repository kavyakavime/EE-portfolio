# Electrical Engineering Portfolio

**[Your Name]**  
Electrical Engineering Student  
[Email] | [LinkedIn] | [GitHub]

---

## Projects

### 1. Software-Defined Oscilloscope & Function Generator

Multi-microcontroller system for characterizing analog filters through automated frequency response analysis.

**Location:** `oscilloscope-filter-characterization/`

**System:**
- ESP32 (function generator with DAC)
- Arduino Nano (10-bit ADC sampling)
- Raspberry Pi (FFT analysis & GUI)
- RC high-pass filter (Device Under Test)

**Results:**
- Measured cutoff frequency: 162 Hz
- Theoretical prediction: 159 Hz
- Error: 1.9% (within component tolerance)

**Skills:** Signal processing, embedded systems, analog circuit design, FFT analysis, measurement instrumentation

**Files:**
- Hardware photos: `hardware-setup/photos/`
- Firmware: `firmware/`
- Analysis software: `software/raspberry_pi_oscilloscope.py`
- Results: `results/`

---

### 2. Sensor & LED Display Projects

Collection of Arduino-based projects demonstrating sensor interfacing, real-time data processing, and visual feedback systems.

**Location:** `sensor-led-projects/`

All projects use 7 LEDs as a bar graph display, with number of lit LEDs proportional to input signal strength.

#### 2.1 Photoresistor Warning System
`photoresistor-warning-system/`

Ambient light monitoring with visual LED indicators (green → yellow → red) and buzzer alarm for low-light conditions.

**Hardware:**
- Photoresistor (analog light sensor)
- 7 LEDs (2 green, 3 yellow, 2 red)
- Piezo buzzer
- Arduino Nano

**Operation:**
- Brighter light → fewer LEDs
- Darker conditions → more LEDs light up
- Buzzer activates when critically dark (<200 ADC value)

**Skills:** Analog sensor reading, threshold detection, visual/audio feedback

---

#### 2.2 Potentiometer LED Bar Graph
`potentiometer-led-control/`

Manual LED intensity control demonstrating ADC conversion and visual feedback.

**Hardware:**
- 10kΩ potentiometer
- 7 LEDs
- Arduino Nano

**Operation:**
- Turn potentiometer clockwise → more LEDs light up
- ADC value (0-1023) mapped to LED count (0-7)
- Real-time visual response to analog input

**Skills:** Analog-to-digital conversion, user interface, LED multiplexing

---

#### 2.3 Motion-Reactive LED Display
`motion-led-display/`

Motion detection system with dynamic LED response for interactive or security applications.

**Hardware:**
- PIR motion sensor
- 7 LEDs
- Arduino Nano

**Operation:**
- Motion detected → LEDs light up proportionally
- No motion → LEDs off or dim
- Real-time response to movement

**Skills:** Digital sensor interfacing, interrupt handling, real-time processing

---

## Technical Skills

**Programming:** C/C++ (Arduino/AVR), Python (NumPy, Matplotlib)  
**Hardware:** Circuit design, breadboarding, multimeter debugging  
**Platforms:** Arduino Nano, ESP32, Raspberry Pi  
**Signal Processing:** FFT analysis, filter characterization, ADC/DAC  
**Tools:** Serial communication, I2C/SPI, timer interrupts

---

## Project Files Structure
```
ee-portfolio/
├── README.md (this file)
├── oscilloscope-filter-characterization/
│   ├── hardware-setup/photos/
│   ├── firmware/
│   ├── software/
│   └── results/
└── sensor-led-projects/
    ├── photoresistor-warning-system/
    ├── potentiometer-led-control/
    └── motion-led-display/
```

---

## Contact

**Email:** [your.email@example.com]  
**LinkedIn:** [linkedin.com/in/yourprofile]  
**GitHub:** [github.com/yourusername]
