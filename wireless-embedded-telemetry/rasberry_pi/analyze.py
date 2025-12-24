import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from collections import deque

# ---------------- CONFIG ----------------
PORT = "/dev/ttyUSB0"
BAUD = 115200
WINDOW = 300
# ----------------------------------------

ser = serial.Serial(PORT, BAUD, timeout=1)

# buffers
latencies = deque(maxlen=WINDOW)
rates = deque(maxlen=WINDOW)
losses = deque(maxlen=WINDOW)

last_seq = None
lost_packets = 0
last_rx_time = None
parse_errors = 0

# latest packet fields
latest_seq = "-"
latest_src = "-"
latest_data = "-"
latest_latency = "-"

# ---------------- PLOT SETUP ----------------
plt.style.use("dark_background")
fig = plt.figure(figsize=(12, 8))
fig.suptitle("📡 Wireless Packet Telemetry Analyzer", fontsize=16)

ax_lat = plt.subplot2grid((3, 2), (0, 0), colspan=2)
ax_rate = plt.subplot2grid((3, 2), (1, 0))
ax_loss = plt.subplot2grid((3, 2), (1, 1))
ax_jit = plt.subplot2grid((3, 2), (2, 0), colspan=2)

lat_line, = ax_lat.plot([], [], lw=2)
rate_line, = ax_rate.plot([], [], lw=2)
loss_line, = ax_loss.plot([], [], lw=2)
jit_line, = ax_jit.plot([], [], lw=2)

ax_lat.set_ylabel("Latency (ms)")
ax_rate.set_ylabel("Packets / sec")
ax_loss.set_ylabel("Lost packets")
ax_jit.set_ylabel("Jitter (ms)")
ax_jit.set_xlabel("Packets")

# 🔥 TEXT PANEL FOR PACKET CONTENTS
packet_text = fig.text(
    0.73, 0.28, "", fontsize=12,
    bbox=dict(facecolor="#111111", edgecolor="white")
)

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.ion()
plt.show()

# ---------------- PARSER ----------------
def parse_line(line):
    # PACKET|107|222000|TXAB|LATENCY:23|COUNT:107
    p = line.split("|")
    if len(p) < 6 or p[0] != "PACKET":
        raise ValueError

    seq = int(p[1])
    src_time = p[2]
    data = p[3]

    latency = None
    for x in p:
        if x.startswith("LATENCY:"):
            latency = int(x.split(":")[1])

    if latency is None:
        raise ValueError

    return seq, src_time, data, latency

# ---------------- MAIN LOOP ----------------
while True:
    try:
        line = ser.readline().decode(errors="ignore").strip()
        if not line.startswith("PACKET|"):
            continue

        try:
            seq, src_time, data, latency = parse_line(line)
            now = time.time()

            # packet loss
            if last_seq is not None and seq != last_seq + 1:
                lost_packets += max(0, seq - last_seq - 1)
            last_seq = seq

            # packet rate
            if last_rx_time is None:
                rate = 0
            else:
                dt = now - last_rx_time
                rate = 1 / dt if dt > 0 else 0
            last_rx_time = now

            # store
            latencies.append(latency)
            rates.append(rate)
            losses.append(lost_packets)

            # jitter
            if len(latencies) > 1:
                jitter_vals = [abs(latencies[i] - latencies[i-1])
                               for i in range(1, len(latencies))]
            else:
                jitter_vals = [0]

            # update plots
            x = range(len(latencies))
            lat_line.set_data(x, latencies)
            rate_line.set_data(x, rates)
            loss_line.set_data(x, losses)
            jit_line.set_data(range(len(jitter_vals)), jitter_vals)

            ax_lat.set_xlim(0, WINDOW)
            ax_rate.set_xlim(0, WINDOW)
            ax_loss.set_xlim(0, WINDOW)
            ax_jit.set_xlim(0, WINDOW)

            ax_lat.set_ylim(0, max(50, max(latencies) * 1.3))
            ax_rate.set_ylim(0, max(5, max(rates) * 1.3))
            ax_loss.set_ylim(0, max(5, lost_packets * 1.3 + 5))
            ax_jit.set_ylim(0, max(5, np.std(latencies) * 4 + 5))

            # 🔥 UPDATE PACKET CONTENT PANEL
            packet_text.set_text(
                " Latest Packet \n"
                "──────────────\n"
                f"SEQ: {seq}\n"
                f"SRC_MS: {src_time}\n"
                f"DATA: {data}\n"
                f"LATENCY: {latency} ms\n"
                f"LOST: {lost_packets}"
            )

            plt.pause(0.01)

        except Exception:
            parse_errors += 1

    except KeyboardInterrupt:
        break

ser.close()
