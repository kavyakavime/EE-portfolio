# Theory and Design Decisions

This document explains the key electrical and communication concepts behind the Multi-MCU Serial Communication Analyzer.

---

## 🔌 Voltage Level Compatibility

### Problem
The Arduino Nano operates at **5V logic**, while the ESP32 uses **3.3V logic**.  
Directly connecting a 5V UART TX pin to an ESP32 RX pin can damage the ESP32.

---

## ✅ Solution: Voltage Divider

A resistor voltage divider was used to safely reduce the Arduino's 5V TX signal.

### Divider Configuration

```
Arduino TX ── 2kΩ ──┬── ESP32 RX
│
1kΩ
│
GND
```

---

## 🧮 Voltage Divider Formula

\[
V_{out} = V_{in} \times \frac{R_2}{R_1 + R_2}
\]

Where:
- \( V_{in} = 5V \)
- \( R_1 = 2kΩ \)
- \( R_2 = 1kΩ \)

\[
V_{out} = 5 \times \frac{1}{3} \approx 1.67V
\]

---

## 🔍 Measured Result

Using a multimeter, the actual measured voltage at the divider midpoint was:

**≈ 2.71 V**

This is:
- Safely below the ESP32’s absolute maximum
- Well above the UART logic-high threshold
- Reliable for stable communication

---

## 🔄 UART Communication Model

- Baud rate: **115200**
- Frame: 8 data bits, no parity, 1 stop bit (8N1)
- Packets are framed using:
  - Fixed header bytes
  - Payload
  - XOR checksum

This ensures:
- Packet boundary detection
- Data integrity validation
- Loss detection via sequence numbers

---

## ⏱ Latency & Jitter Measurement

The ESP32 timestamps each packet:
- Immediately on receive
- Immediately before forwarding

Latency is computed as:

\[
Latency = t_{tx} - t_{rx}
\]

Jitter is defined as the variation between successive latency measurements.

---

## 📈 Why This Approach Works

This system models real instrumentation techniques used in:
- Logic analyzers
- Network analyzers
- Embedded protocol debugging tools

Rather than relying on assumptions, it **measures actual behavior** across real hardware boundaries.

---

## 🧠 Key Takeaway

Reliable embedded communication is not just about software.  
Electrical safety, timing, framing, and buffering all matter—and this project demonstrates how they interact in a measurable, visual way.
