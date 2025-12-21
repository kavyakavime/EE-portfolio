# Multi-MCU Serial Communication Analyzer

A real-time serial packet analysis system built using an Arduino Nano, ESP32, and Raspberry Pi.  
This project explores **embedded communication pipelines**, packet integrity, latency, and jitter—conceptually similar to how packet sniffing tools like **Wireshark** analyze network traffic, but implemented at the **microcontroller UART level**.

---

## 🔍 Motivation

While studying cybersecurity and using tools like **Wireshark**, I became interested in how packet inspection and timing analysis actually work beneath high-level protocols.  
This project was built to explore those same ideas in an **embedded systems context**, where constraints such as baud rate, voltage levels, buffering, and processing delay matter.

Instead of Ethernet packets, this system analyzes **raw UART packets** moving across multiple MCUs.

---

## 🧠 System Overview

- **Arduino Nano**  
  Generates structured binary packets at a fixed rate.

- **ESP32**  
  Acts as a transparent relay, timestamping packets on receive and transmit.

- **Raspberry Pi**  
  Receives packets, validates integrity, computes:
  - Throughput
  - Latency
  - Jitter
  - Packet loss  
  and visualizes results in real time using Python.

---

## ⚙️ Hardware Design

- UART communication at **115200 baud**
- Safe 5V → 3.3V level shifting using a **resistor voltage divider**
- Dedicated UART lines (no USB serial contention)
- Common ground shared across all devices

A full wiring photo and divider details are included in the `hardware/` directory.

---

## 📊 Results

### Final Statistics (Longest Run)

- **Total packets received:** 2144  
- **Packets lost:** 0  
- **Packet loss rate:** 0.00%  
- **Average latency:** 26.100 ms  
- **Average jitter:** ~0.007 ms  
- **Sustained packet rate:** ~10 packets/sec  

### Visualizations

The analyzer produces:
- Throughput vs time
- ESP32 relay latency per packet
- Jitter (latency variation)
- Live runtime statistics panel

Example outputs are included in the `results/` folder.

---

## 🔬 Why This Matters

This project mirrors real-world tools and concepts used in:
- Packet sniffing
- Embedded protocol debugging
- Performance analysis
- Serial communication reliability testing

It demonstrates how **low-level hardware decisions** (timing, voltage, buffering) directly affect system-level performance—something that high-level software often abstracts away.

---

## 🚀 Future Improvements

- Higher packet rates
- CRC instead of XOR checksum
- Support for SPI / I²C comparison
- Trigger-based capture
- Packet drop injection for stress testing

---

## 🧑‍💻 Author

Built by **[Your Name]**  
Focus: Embedded Systems, Low-Level Communication, Instrumentation

License: MIT

