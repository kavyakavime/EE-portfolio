# have the matplot dependency installed
# run this command 'pip3 install pyserial matplotlib numpy'
#!/usr/bin/env python3
"""
Multi-MCU Serial Communication Analyzer
Real-time packet analysis with Wireshark-like metrics
"""

import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from collections import deque
import numpy as np

# Configuration
ESP32_PORT = '/dev/ttyUSB0'  # Change to your ESP32 port
BAUD_RATE = 115200
WINDOW_SIZE = 50  # Number of packets to display

# Data storage
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

# Setup serial connection
try:
    ser = serial.Serial(ESP32_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to ESP32 on {ESP32_PORT}")
except Exception as e:
    print(f"Error connecting: {e}")
    exit(1)

# Setup plots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Multi-MCU Serial Communication Analyzer', fontsize=16, fontweight='bold')

def parse_packet(line):
    """Parse packet: SEQ|NANO_TIME|PAYLOAD|CHECKSUM|ESP_RX_TIME|ESP_TX_TIME"""
    try:
        parts = line.strip().split('|')
        
        if parts[0] == "STATUS":
            return None  # Ignore status messages
        
        if len(parts) >= 6:
            return {
                'seq': int(parts[0]),
                'nano_time': int(parts[1]),
                'payload': parts[2],
                'checksum': int(parts[3]),
                'esp_rx_time': int(parts[4]),
                'esp_tx_time': int(parts[5]),
                'pi_time': time.time()
            }
    except Exception as e:
        print(f"Parse error: {e} | Line: {line}")
    return None

def calculate_metrics(packet):
    """Calculate latency and jitter"""
    global packets_received, packets_lost, last_seq, total_latency
    
    packets_received += 1
    seq = packet['seq']
    
    # Detect packet loss
    if last_seq != -1 and seq != last_seq + 1:
        lost = seq - last_seq - 1
        packets_lost += lost
        print(f"⚠️  Packet loss detected! Missing: {lost} packets")
    
    last_seq = seq
    
    # Calculate ESP32 relay latency (microseconds)
    esp_latency = packet['esp_tx_time'] - packet['esp_rx_time']
    latencies.append(esp_latency / 1000.0)  # Convert to milliseconds
    total_latency += esp_latency
    
    # Calculate jitter (variation in latency)
    if len(latencies) > 1:
        jitter = abs(latencies[-1] - latencies[-2])
        jitters.append(jitter)
    
    packet_times.append(time.time() - start_time)
    sequence_numbers.append(seq)

def update_plots(frame):
    """Update all plots in real-time"""
    
    # Read new packets
    while ser.in_waiting:
        try:
            line = ser.readline().decode('utf-8', errors='ignore')
            packet = parse_packet(line)
            if packet:
                calculate_metrics(packet)
        except Exception as e:
            print(f"Read error: {e}")
    
    # Clear all axes
    ax1.clear()
    ax2.clear()
    ax3.clear()
    ax4.clear()
    
    # Plot 1: Throughput over time
    ax1.set_title('Throughput (packets/sec)', fontweight='bold')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Packets')
    if len(sequence_numbers) > 1:
        ax1.plot(packet_times, sequence_numbers, 'b-', linewidth=2)
        ax1.fill_between(packet_times, sequence_numbers, alpha=0.3)
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: ESP32 Relay Latency
    ax2.set_title('ESP32 Relay Latency', fontweight='bold')
    ax2.set_xlabel('Packet Number')
    ax2.set_ylabel('Latency (ms)')
    if len(latencies) > 0:
        ax2.plot(range(len(latencies)), latencies, 'r-', linewidth=2, label='Latency')
        avg_latency = np.mean(latencies)
        ax2.axhline(avg_latency, color='orange', linestyle='--', label=f'Avg: {avg_latency:.3f}ms')
        ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Jitter Analysis
    ax3.set_title('Jitter (Latency Variation)', fontweight='bold')
    ax3.set_xlabel('Packet Number')
    ax3.set_ylabel('Jitter (ms)')
    if len(jitters) > 0:
        ax3.plot(range(len(jitters)), jitters, 'g-', linewidth=2)
        ax3.fill_between(range(len(jitters)), jitters, alpha=0.3, color='green')
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Statistics Summary
    ax4.axis('off')
    runtime = time.time() - start_time
    packet_rate = packets_received / runtime if runtime > 0 else 0
    loss_rate = (packets_lost / (packets_received + packets_lost) * 100) if packets_received > 0 else 0
    avg_latency = np.mean(latencies) if len(latencies) > 0 else 0
    avg_jitter = np.mean(jitters) if len(jitters) > 0 else 0
    
    stats_text = f"""
    📊 REAL-TIME STATISTICS
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Runtime:          {runtime:.1f}s
    Packets Received: {packets_received}
    Packets Lost:     {packets_lost}
    Loss Rate:        {loss_rate:.2f}%
    
    Packet Rate:      {packet_rate:.2f} pkt/s
    Avg Latency:      {avg_latency:.3f} ms
    Avg Jitter:       {avg_jitter:.3f} ms
    
    📈 Throughput:    {packet_rate * 30:.0f} bytes/s
    """
    
    ax4.text(0.1, 0.5, stats_text, fontsize=12, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round', 
             facecolor='lightblue', alpha=0.8))
    
    plt.tight_layout()

# Start real-time animation
print("\n🚀 Starting Multi-MCU Communication Analyzer...")
print("📡 Monitoring packets from Arduino → ESP32 → Raspberry Pi")
print("Press Ctrl+C to stop\n")

try:
    ani = FuncAnimation(fig, update_plots, interval=100, cache_frame_data=False)
    plt.show()
except KeyboardInterrupt:
    print("\n\n📊 Final Statistics:")
    print(f"Total packets: {packets_received}")
    print(f"Packets lost: {packets_lost}")
    print(f"Average latency: {np.mean(latencies):.3f} ms")
    ser.close()
