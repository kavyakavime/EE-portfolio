# Software-Defined Oscilloscope & Function Generator

A multi-microcontroller instrumentation system for automated frequency response analysis of analog filters. Built with ESP32, Arduino Nano, and Raspberry Pi.



## Overview

This project implements a **software-defined oscilloscope and function generator** to experimentally characterize an RC high-pass filter. The system generates programmable test signals, digitizes the filter response, and performs FFT analysis to estimate gain vs. frequency.

**What it does:**
- Generates sine waves using the ESP32 DAC
- Samples **both input and output** using the Arduino Nano 10-bit ADC
- Real-time input vs output waveform display on Raspberry Pi
- Frequency sweep measurement → Bode magnitude plot
- Compares measured response against the theoretical RC high-pass model

**Skills demonstrated:** Embedded systems, signal processing, analog circuit design, measurement instrumentation, error analysis



## System Architecture
```
ESP32 (Function Generator)
│
│ Vin(t)
▼
RC High-Pass Filter 
│
│ Vout(t)
▼
Arduino Nano (ADC: Vin + Vout)
│
│ USB Serial
▼
Raspberry Pi 5 (Plotting + FFT + Sweep Analysis)
```


**Design rationale:**
- **ESP32** → built-in 8-bit DAC for waveform generation
- **Arduino Nano** → built-in 10-bit ADC (Raspberry Pi has no native ADC)
- **Raspberry Pi** → real-time plotting + FFT + sweep automation

---

## Hardware Design

### ESP32 Function Generator
- 8-bit DAC output (0–3.3 V)
- Lookup-table sine wave generation

### High-Pass Filter (Device Under Test)
- **Components:** R = 10 kΩ, C = 0.1 µF
- **Theoretical cutoff:**  
  $f_c = \frac{1}{2\pi RC} \approx \frac{1}{2\pi(10,000)(0.1\mu F)} \approx 159\ \text{Hz}$
  
- **Tested frequency range (current setup):** ~50 Hz to 1000 Hz  
  (limited by Arduino sampling rate and measurement method)

### Arduino Nano ADC Front-End
- 10-bit ADC sampling streamed to Raspberry Pi over USB serial
- Two-channel measurement:
  - Channel 1: Vin (input from ESP32 DAC)
  - Channel 2: Vout (filter output node)


## Software Architecture

### Raspberry Pi Analysis & GUI
- Python + Matplotlib for real-time oscilloscope plotting
- FFT using NumPy for frequency-domain inspection
- Automated sweep script computes RMS gain per test frequency
- Exports CSV for measured vs theoretical comparison

**Processing flow:** Arduino streams ADC samples → Pi buffers → RMS + FFT computed → plots/CSV generated


## Results

### Time-Domain Verification
Real-time plots show:
- **Vin** larger than **Vout**, confirming attenuation at lower frequencies
- Output amplitude increases as frequency increases, consistent with high-pass behavior

### Frequency Response 
- Theoretical curve uses the 1st-order RC high-pass model with **f_c ≈ 159 Hz**
- Measured gain points (blue) rise with frequency, but the measured “passband” gain plateaus around **~ −4 dB** (near 800–1000 Hz), rather than reaching 0 dB.

### Bode Magnitude Comparison (Measured vs. Theoretical)

The Bode magnitude plot compares the **measured gain** of the RC high-pass filter with the **theoretical first-order response** (dashed curve, \( f_c \approx 159 \,\text{Hz} \)). The measured data (blue points) shows strong low-frequency attenuation and increasing gain with frequency, consistent with expected high-pass behavior.

While the overall shape and slope (~20 dB/decade) match theory, the measured response exhibits a **constant gain offset**, with the passband saturating near **−4 dB** instead of 0 dB. This offset is attributed to non-ideal DAC amplitude, ADC reference scaling, and measurement-chain loading effects.

Using the measured passband as a reference, the **measured cutoff frequency** (passband −3 dB) occurs near **~400 Hz**. Despite the offset, the close agreement in response shape validates the filter operation and the software-defined measurement system.



## Error Analysis 

Real measurement systems have limitations. These were the dominant sources of error in this build:

### 1) ADC Reference / Voltage Scaling Mismatch (Biggest)
Arduino Nano ADC readings are referenced to **~5 V** by default (AVcc).  
If the Raspberry Pi software converts ADC counts assuming **3.3 V**, then the plotted “volts” will be wrong (and can even appear >3.3 V).  
This can shift apparent amplitudes and distort gain, especially if Vin and Vout aren’t scaled consistently.


### 2) Sampling Rate Limit + Aliasing
Your Arduino sampling is around ~2 kHz in many examples → Nyquist ≈ 1 kHz.  
As you approach higher frequencies, amplitude and RMS estimation can become inaccurate.



### 3) Serial Timing Jitter (Non-uniform Sampling)
USB serial printing is not a perfect timer. The time between samples is not perfectly constant, which hurts FFT accuracy and can add noise/spurs.


### 4) ESP32 DAC Quantization + Stepping (8-bit)
The ESP32 DAC is 8-bit → sine wave is “stair-stepped,” producing harmonics.
Those harmonics show up in FFT and can slightly affect RMS gain measurements.


### 5) Component Tolerances + Breadboard Parasitics
R and C tolerances (±5% resistor, ±10–20% capacitor) change true cutoff frequency.  
Breadboard stray capacitance/resistance also shifts response.



## Future Improvements
- Calibrate ADC scaling using measured AVcc
- Replace serial println with binary streaming
- Increase sampling rate + windowed FFT
- Add external ADC for higher bandwidth
- Add phase measurement (cross-correlation)

---

## Key Takeaway

This project demonstrates **end-to-end instrumentation design** across embedded signal generation, analog filtering, digital sampling, and frequency-domain analysis—while documenting real-world constraints (ADC reference, sampling limits, DAC distortion) and their measurable impact on results.
