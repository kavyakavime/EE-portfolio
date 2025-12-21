# Theory and Design Decisions

This document explains the electrical and communication concepts behind the Multi-MCU Serial Communication Analyzer and the reasoning behind key design choices.

---

## Voltage Level Compatibility

### Problem

The Arduino Nano operates at **5 V logic levels**, while the ESP32 uses **3.3 V logic**.  
Directly connecting a 5 V UART TX pin from the Arduino to the ESP32 RX pin can overstress and permanently damage the ESP32.

---

## Solution: Voltage Divider

A passive resistor voltage divider was used to safely reduce the Arduino’s TX voltage to a level compatible with the ESP32.

### Divider Configuration

```
Arduino TX ── 2 kΩ ──┬── ESP32 RX
│
1 kΩ
│
GND
```


This approach was selected because it is simple, reliable at UART speeds, and requires no active components.

---

## Voltage Divider Calculation

The output voltage of a resistor divider is calculated as:

$V_{out} = V_{in} \times \frac{R_2}{R_1 + R_2}$

Where:
- $\( V_{in} = 5 \, V \)$
- $\( R_1 = 2 \, k\Omega \)$
- $\( R_2 = 1 \, k\Omega \)$

$V_{out} = 5 \times \frac{1}{3} \approx 1.67 \, V$

---

## Measured Result

The actual voltage measured at the divider midpoint was approximately:

**2.7 V**

The difference between the theoretical and measured values is attributed to:
- ESP32 RX input impedance
- Resistor tolerances
- Measurement loading effects

This voltage is:
- Below the ESP32’s absolute maximum input rating
- Above the UART logic-high threshold
- Stable for reliable serial communication

---

## UART Communication Model

The system uses standard asynchronous serial communication with the following parameters:

- Baud rate: **115200**
- Frame format: **8 data bits, no parity, 1 stop bit (8N1)**

Each packet consists of:
- A fixed header
- Payload data
- An XOR checksum
- A sequence number

This structure enables:
- Clear packet boundary detection
- Data integrity validation
- Packet loss detection through sequence tracking

---

## Latency and Jitter Measurement

The ESP32 timestamps each packet at two points:
1. Immediately upon reception
2. Immediately before forwarding

Latency is calculated as:

$Latency = t_{tx} - t_{rx}$

Jitter is defined as the absolute difference between consecutive latency measurements.

---

## Design Rationale

This system models techniques commonly used in professional instrumentation such as:
- Logic analyzers
- Network analyzers
- Embedded protocol debugging tools

Rather than relying on assumptions, the design measures real timing and behavior across actual hardware boundaries.

---

## Key Takeaway

Reliable embedded communication requires careful consideration of both hardware and software.  
Voltage levels, timing accuracy, packet framing, and buffering all directly affect system reliability.  
This project demonstrates how these factors interact and how they can be measured and visualized.
