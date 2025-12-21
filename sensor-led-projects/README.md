# Sensor & LED Display Projects

Collection of Arduino-based projects demonstrating sensor interfacing, real-time data processing, and visual feedback systems using 7-LED bar graph displays.

---

## Overview

Three projects exploring different input methods (analog sensor, manual control, motion detection) with a common output: a 7-LED bar graph that responds proportionally to input signal strength.

**Common Hardware:**
- Arduino Nano
- 7 LEDs with 220Ω resistors
- Breadboard & jumper wires
- Active Buzzer

**Skills Demonstrated:**
- Analog and digital sensor interfacing
- Real-time ADC reading and processing
- LED control and multiplexing
- Threshold detection and visual feedback
- Arduino programming in C/C++

---

## Projects

### 1. Photoresistor Warning System
**Location:** `photoresistor-warning-system/`

Ambient light monitoring system with color-coded LED warnings and audible alarm for low-light conditions.

**Additional Hardware:**
- Photoresistor (analog light sensor)

**How it works:**
- Reads ambient light level via photoresistor (0-1023 ADC range)
- LEDs light up progressively as room gets darker
- 2 green LEDs → 3 yellow LEDs → 2 red LEDs
- Buzzer activates when light drops below critical threshold (~200 ADC)

**Key Features:**
- Averaged readings for stability (5-sample moving average)
- Configurable threshold levels for each LED
- Visual gradient: green (bright) → yellow (dim) → red (dark)

**Code:** `code/photoresistor_warning.ino`  
**Photos:** `photos/` (bright room vs dark room comparison)

---

### 2. Potentiometer LED Bar Graph
**Location:** `potentiometer-led-control/`

Manual LED intensity control demonstrating analog-to-digital conversion and user-controlled visual feedback.

**Additional Hardware:**
- 10kΩ potentiometer

**How it works:**
- Potentiometer position controls number of lit LEDs
- ADC reads pot value (0-1023)
- Value mapped to LED count (0-7 LEDs)
- Immediate visual response to knob rotation

**Key Features:**
- Direct ADC-to-LED mapping
- Smooth, linear response
- User-controlled intensity adjustment

**Code:** `code/potentiometer_led_bar.ino`  
**Photos:** `photos/` (low setting vs high setting)

---

### 3. Motion-Reactive LED Display
**Location:** `motion-led-display/`

Motion detection system with dynamic LED response for security monitoring or interactive installations.

**Additional Hardware:**
- PIR motion sensor (or alternative motion detector)

**How it works:**
- Motion sensor detects movement in detection range
- LEDs respond to motion events
- Number of LEDs indicates motion intensity or duration
- Returns to idle state when no motion detected

**Key Features:**
- Real-time motion response
- Digital sensor interfacing
- Event-driven LED control

**Code:** `code/motion_detector_leds.ino`  
**Photos:** `photos/` (motion detected vs idle state)

---

## Common Circuit Architecture

## Contact

**Email:** [your.email@example.com]  
**LinkedIn:** [linkedin.com/in/yourprofile]  
**GitHub:** [github.com/yourusername]
