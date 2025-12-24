#  Wireless Embedded Telemetry System

A distributed embedded system that streams sensor telemetry from an **Arduino Nano** over **UART → ESP-NOW (ESP32 → ESP32)** and visualizes packet timing and loss on a **Raspberry Pi**, with real-time status shown on a **parallel OLED/LCD**.

**Features**
- Structured telemetry packets (sequence, timestamp, sensor data)
- UART voltage-level safe interface (5V → 3.3V)
- Wireless transport using ESP-NOW (fixed channel)
- End-to-end latency measurement & packet loss detection
- Live OLED/LCD display
- CSV logging and analysis on Raspberry Pi

**Pipeline**
Arduino → ESP32 (UART) → ESP32 (ESP-NOW) → OLED + Raspberry Pi


Built to explore **embedded packet inspection, timing, and reliability**, inspired by network analysis tools like Wireshark.
