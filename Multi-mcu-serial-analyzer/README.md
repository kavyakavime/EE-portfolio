# Multi-MCU Serial Communication Analyzer

A real-time serial packet analysis system built using an Arduino Nano, ESP32, and Raspberry Pi.

This project explores embedded communication pipelines, packet integrity, latency, and jitter. Conceptually, it is similar to how packet analysis tools such as Wireshark inspect network traffic, but implemented at the UART level across multiple microcontrollers.

---

## Motivation

While studying cybersecurity and working with tools like Wireshark, I became interested in how packet inspection, timing analysis, and loss detection actually function beneath high-level protocols.

This project was built to explore those same concepts in an embedded systems context, where factors such as baud rate, voltage compatibility, buffering, and processing latency have a direct and observable impact on system behavior.

Instead of Ethernet frames, the system analyzes raw UART packets transmitted across multiple MCUs.

---

## System Overview

The system consists of three devices connected in a serial communication pipeline:

- **Arduino Nano**  
  Generates structured packets at a fixed transmission rate.

- **ESP32**  
  Acts as a transparent relay between devices, timestamping packets on reception and again immediately before forwarding.

- **Raspberry Pi**  
  Receives packets, validates integrity, computes performance metrics, and visualizes results in real time using Python.

The Raspberry Pi calculates:
- Throughput
- End-to-end latency
- Jitter
- Packet loss

---

## Hardware Design

- UART communication at **115200 baud**
- Safe 5 V to 3.3 V level shifting using a resistor voltage divider
- Dedicated hardware UART lines (no USB serial contention)
- Common ground shared between all devices

Detailed wiring diagrams and voltage divider measurements are provided in the `hardware/` directory.

---

## Results

### Final Statistics (Longest Continuous Run)

- **Total packets received:** 2144  
- **Packets lost:** 0  
- **Packet loss rate:** 0.00%  
- **Average latency:** 26.100 ms  
- **Average jitter:** approximately 0.007 ms  
- **Sustained packet rate:** approximately 10 packets per second  

### Visual Output

The analyzer produces real-time visualizations for:
- Throughput over time
- ESP32 relay latency per packet
- Jitter (latency variation)
- Live runtime statistics

Example plots and screenshots are included in the `results/` directory.

---

## Why This Matters

This project mirrors real-world techniques used in:
- Packet sniffing and inspection
- Embedded protocol debugging
- Performance characterization
- Serial communication reliability testing

It demonstrates how low-level hardware and timing decisions directly influence system-level performance, something that is often abstracted away by higher-level software stacks.

---

## Future Improvements

Planned extensions include:
- Higher packet transmission rates
- CRC-based error detection instead of XOR checksums
- Support for SPI and I²C for protocol comparison
- Trigger-based capture and filtering
- Intentional packet drop injection for stress testing

---
