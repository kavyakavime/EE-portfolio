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

