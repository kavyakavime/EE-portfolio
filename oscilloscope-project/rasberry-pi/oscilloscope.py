import serial
import numpy as np
import csv
import time

SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
VREF = 3.3
SAMPLES_PER_FREQ = 200

# Different sweep frequencies.
frequencies = [100, 200, 500, 1000, 2000, 5000]

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # time for arduino to start

results = []

for freq in frequencies:
    vin_samples = []
    vout_samples = []
    print(f"Collecting {SAMPLES_PER_FREQ} samples at {freq} Hz")

    # Read fixed number of samples
    while len(vin_samples) < SAMPLES_PER_FREQ:
        line = ser.readline().decode(errors='ignore').strip()
        if ',' in line:
            try:
                vin_str, vout_str = line.split(',')
                vin_samples.append(int(vin_str)/1023*VREF)
                vout_samples.append(int(vout_str)/1023*VREF)
            except ValueError:
                continue

    # Computing the rms values
    vin_rms = np.sqrt(np.mean(np.array(vin_samples)**2))
    vout_rms = np.sqrt(np.mean(np.array(vout_samples)**2))
    gain_db = 20 * np.log10(vout_rms / vin_rms)

    results.append((freq, vin_rms, vout_rms, gain_db))
    print(f"Freq={freq} Hz, Vin={vin_rms:.3f}V, Vout={vout_rms:.3f}V, Gain={gain_db:.2f} dB")

ser.close()

# Save CSV for later analysis
with open("bode_results.csv","w",newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Frequency (Hz)","Vin RMS (V)","Vout RMS (V)","Gain (dB)"])
    writer.writerows(results)
print("Saved bode_results.csv")
