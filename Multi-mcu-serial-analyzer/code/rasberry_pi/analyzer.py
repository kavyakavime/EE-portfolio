"""
Multi-MCU Serial Communication Analyzer

Real-time packet analysis for embedded systems.
"""

import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import numpy as np

ESP32_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200
WINDOW_SIZE = 50  # Number of packets displayed

# Data buffers
packet_times = deque(maxlen=WINDOW_SIZE)
latencies = deque(maxlen=WINDOW_SIZE)
jitters = deque(maxlen=WINDOW_SIZE)
sequence_numbers = deque(maxlen=WINDOW_SIZE)

# Statistics
packets_received = 0
packets_lost = 0
last_seq = -1
total_latency = 0
start_time = time.time()

# Serial connection
try:
    ser = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to ESP32 on {ESP32_PORT}")
except Exception as e:
    print(f"Failed to connect to serial port: {e}")
    exit(1)

# Plot setup
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Multi-MCU Serial Communication Analyzer", fontsize=16, fontweight="bold")


def parse_packet(line):
    """
    Packet format:
    SEQ|NANO_TIME|PAYLOAD|CHECKSUM|ESP_RX_TIME|ESP_TX_TIME
    """
    try:
        parts = line.strip().split("|")

        if parts[0] == "STATUS":
            return None

        if len(parts) >= 6:
            return {
                "seq": int(parts[0]),
                "nano_time": int(parts[1]),
                "payload": parts[2],
                "checksum": int(parts[3]),
                "esp_rx_time": int(parts[4]),
                "esp_tx_time": int(parts[5]),
                "pi_time": time.time(),
            }
    except Exception as e:
        print(f"Packet parse error: {e} | Raw line: {line}")

    return None


def calculate_metrics(packet):
    global packets_received, packets_lost, last_seq, total_latency

    packets_received += 1
    seq = packet["seq"]

    # Packet loss detection
    if last_seq != -1 and seq != last_seq + 1:
        lost = seq - last_seq - 1
        packets_lost += lost
        print(f"Packet loss detected: {lost} packets missing")

    last_seq = seq

    # ESP32 relay latency (microseconds → milliseconds)
    esp_latency_us = packet["esp_tx_time"] - packet["esp_rx_time"]
    esp_latency_ms = esp_latency_us / 1000.0
    latencies.append(esp_latency_ms)
    total_latency += esp_latency_us

    # Jitter calculation
    if len(latencies) > 1:
        jitters.append(abs(latencies[-1] - latencies[-2]))

    packet_times.append(time.time() - start_time)
    sequence_numbers.append(seq)


def update_plots(frame):
    # Read incoming serial data
    while ser.in_waiting:
        try:
            line = ser.readline().decode("utf-8", errors="ignore")
            packet = parse_packet(line)
            if packet:
                calculate_metrics(packet)
        except Exception as e:
            print(f"Serial read error: {e}")

    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()

    # Throughput
    ax1.set_title("Throughput (packets/sec)")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Packets")
    if len(sequence_numbers) > 1:
        ax1.plot(packet_times, sequence_numbers, linewidth=2)
        ax1.fill_between(packet_times, sequence_numbers, alpha=0.3)
    ax1.grid(True, alpha=0.3)

    # Latency
    ax2.set_title("ESP32 Relay Latency")
    ax2.set_xlabel("Packet Index")
    ax2.set_ylabel("Latency (ms)")
    if latencies:
        ax2.plot(range(len(latencies)), latencies, linewidth=2)
        avg_latency = np.mean(latencies)
        ax2.axhline(avg_latency, linestyle="--", label=f"Avg: {avg_latency:.3f} ms")
        ax2.legend()
    ax2.grid(True, alpha=0.3)

    # Jitter
    ax3.set_title("Jitter")
    ax3.set_xlabel("Packet Index")
    ax3.set_ylabel("Jitter (ms)")
    if jitters:
        ax3.plot(range(len(jitters)), jitters, linewidth=2)
        ax3.fill_between(range(len(jitters)), jitters, alpha=0.3)
    ax3.grid(True, alpha=0.3)

    # Statistics
    ax4.axis("off")
    runtime = time.time() - start_time
    packet_rate = packets_received / runtime if runtime > 0 else 0
    loss_rate = (
        packets_lost / (packets_received + packets_lost) * 100
        if packets_received > 0
        else 0
    )
    avg_latency = np.mean(latencies) if latencies else 0
    avg_jitter = np.mean(jitters) if jitters else 0

    stats_text = (
        f"Runtime:           {runtime:.1f} s\n"
        f"Packets received:  {packets_received}\n"
        f"Packets lost:      {packets_lost}\n"
        f"Loss rate:         {loss_rate:.2f} %\n\n"
        f"Packet rate:       {packet_rate:.2f} pkt/s\n"
        f"Average latency:   {avg_latency:.3f} ms\n"
        f"Average jitter:    {avg_jitter:.3f} ms\n"
    )

    ax4.text(
        0.05,
        0.5,
        stats_text,
        fontsize=12,
        family="monospace",
        verticalalignment="center",
        bbox=dict(boxstyle="round", facecolor="lightgray", alpha=0.8),
    )

    plt.tight_layout()


print("Starting serial communication analyzer")
print("Press Ctrl+C to stop")

try:
    ani = FuncAnimation(fig, update_plots, interval=100, cache_frame_data=False)
    plt.show()
except KeyboardInterrupt:
    print("Stopping analyzer")
    print(f"Total packets received: {packets_received}")
    print(f"Packets lost: {packets_lost}")
    if latencies:
        print(f"Average latency: {np.mean(latencies):.3f} ms")
    ser.close()
