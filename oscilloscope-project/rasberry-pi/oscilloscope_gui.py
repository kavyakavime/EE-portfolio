
import argparse
import csv
import math
import time
from collections import deque

import numpy as np
import serial
import matplotlib.pyplot as plt




FRAME_HDR = b"\xAA\x55"
FRAME_LEN = 2 + 2 + 2  # vin(2) + vout(2) after header

R_OHMS = 10_000.0
C_FARADS = 0.1e-6


ADC_VREF = 5.0  # default Arduino AREF
ADC_MAX = 1023.0


def read_one_frame(ser: serial.Serial):
    # Find header
    while True:
        b = ser.read(1)
        if not b:
            return None
        if b == FRAME_HDR[0:1]:
            b2 = ser.read(1)
            if b2 == FRAME_HDR[1:2]:
                break

    payload = ser.read(FRAME_LEN)
    if len(payload) != FRAME_LEN:
        return None

    vin = payload[0] | (payload[1] << 8)
    vout = payload[2] | (payload[3] << 8)
    return vin, vout


def adc_to_volts(adc_val: np.ndarray) -> np.ndarray:
    return (adc_val / ADC_MAX) * ADC_VREF


def hp_theoretical_gain_phase(freq_hz: float, R: float, C: float):
    """High-pass: H(jw) = jwRC / (1 + jwRC)"""
    w = 2.0 * math.pi * freq_hz
    x = w * R * C
    mag = x / math.sqrt(1.0 + x * x)
    gain_db = 20.0 * math.log10(mag) if mag > 0 else -999.0
    # phase = arg(jwRC) - arg(1+jwRC) = 90deg - atan(wRC) = atan(1/(wRC))
    phase_deg = math.degrees(math.atan2(1.0, x))  # safe for x=0
    return gain_db, phase_deg


def rms_ac(signal: np.ndarray) -> float:
    """RMS of AC component (remove DC offset first)."""
    s = signal - np.mean(signal)
    return float(np.sqrt(np.mean(s * s)))


def phase_at_freq(vin: np.ndarray, vout: np.ndarray, fs_hz: float, freq_hz: float) -> float:
    n = len(vin)
    t = np.arange(n) / fs_hz
    ref = np.exp(-1j * 2 * np.pi * freq_hz * t)

    vin_c = np.dot((vin - np.mean(vin)), ref)
    vout_c = np.dot((vout - np.mean(vout)), ref)

    # phase difference = angle(vout) - angle(vin)
    ph = np.angle(vout_c) - np.angle(vin_c)
    # wrap to [-pi, pi]
    ph = (ph + np.pi) % (2 * np.pi) - np.pi
    return float(np.degrees(ph))


def open_serial(port: str, baud: int):
    ser = serial.Serial(port, baudrate=baud, timeout=1)
    time.sleep(1.5)  # allow board reset
    ser.reset_input_buffer()
    return ser


def mode_live(args):
    ser = open_serial(args.arduino, 230400)

    fs_hz = args.fs
    nplot = args.nplot

    vin_buf = deque(maxlen=nplot)
    vout_buf = deque(maxlen=nplot)

    plt.ion()
    fig, ax = plt.subplots()
    line_in, = ax.plot([], [], label="Vin (A0) [V]")
    line_out, = ax.plot([], [], label="Vout (A1) [V]")

    ax.set_title("Real-time Input vs Output (Arduino ADC → Raspberry Pi)")
    ax.set_xlabel("Sample")
    ax.set_ylabel("Volts (scaled from Arduino ADC)")
    ax.legend()

    last_fft_time = 0
    fig2, ax2 = None, None

    try:
        while True:
            fr = read_one_frame(ser)
            if fr is None:
                continue
            vin_adc, vout_adc = fr
            vin_buf.append(vin_adc)
            vout_buf.append(vout_adc)

            if len(vin_buf) >= 50:
                vin_v = adc_to_volts(np.array(vin_buf, dtype=np.float32))
                vout_v = adc_to_volts(np.array(vout_buf, dtype=np.float32))

                line_in.set_data(range(len(vin_v)), vin_v)
                line_out.set_data(range(len(vout_v)), vout_v)
                ax.set_xlim(0, len(vin_v))
                ax.set_ylim(0, 3.6)  # show 0..3.3V nicely
                plt.pause(0.001)

                # Optional FFT window (updates ~2x per second)
                if args.fft and (time.time() - last_fft_time) > 0.5 and len(vout_v) >= 256:
                    last_fft_time = time.time()
                    if fig2 is None:
                        fig2, ax2 = plt.subplots()
                        ax2.set_title("Output FFT (Magnitude)")
                        ax2.set_xlabel("Hz")
                        ax2.set_ylabel("Magnitude")
                    ax2.clear()
                    n = len(vout_v)
                    w = np.hanning(n)
                    yf = np.fft.rfft((vout_v - np.mean(vout_v)) * w)
                    xf = np.fft.rfftfreq(n, 1.0 / fs_hz)
                    ax2.plot(xf, np.abs(yf))
                    ax2.set_xlim(0, min(5000, fs_hz / 2))
                    plt.pause(0.001)

    except KeyboardInterrupt:
        print("\n[live] exiting...")
    finally:
        ser.close()


def mode_sweep(args):
    # Open both serial ports
    ar = open_serial(args.arduino, 230400)
    es = open_serial(args.esp32, 115200)

    fs_hz = args.fs
    n = args.nsamples
    settle_s = args.settle

    freqs = np.arange(args.fstart, args.fend + 0.5 * args.fstep, args.fstep, dtype=float)

    rows = []
    try:
        for f in freqs:
            # Command ESP32 frequency
            cmd = f"F {f:.2f}\n".encode()
            es.write(cmd)
            time.sleep(settle_s)

            # Collect samples
            vin = np.empty(n, dtype=np.float32)
            vout = np.empty(n, dtype=np.float32)
            got = 0
            t0 = time.time()
            while got < n:
                fr = read_one_frame(ar)
                if fr is None:
                    # prevent infinite hang
                    if time.time() - t0 > 5:
                        raise RuntimeError("Timeout waiting for Arduino frames. Check wiring/baud/port.")
                    continue
                vin_adc, vout_adc = fr
                vin[got] = vin_adc
                vout[got] = vout_adc
                got += 1

            vin_v = adc_to_volts(vin)
            vout_v = adc_to_volts(vout)

            vin_rms = rms_ac(vin_v)
            vout_rms = rms_ac(vout_v)
            gain_db = 20.0 * math.log10(vout_rms / vin_rms) if vin_rms > 0 else -999.0

            ph_meas = phase_at_freq(vin_v, vout_v, fs_hz=fs_hz, freq_hz=float(f))
            theo_gain_db, theo_phase = hp_theoretical_gain_phase(float(f), R_OHMS, C_FARADS)

            rows.append({
                "frequency_hz": float(f),
                "vin_rms_v": vin_rms,
                "vout_rms_v": vout_rms,
                "gain_db_measured": gain_db,
                "phase_deg_measured": ph_meas,
                "gain_db_theoretical": theo_gain_db,
                "phase_deg_theoretical": theo_phase,
            })

            print(f"[sweep] f={f:7.1f} Hz | gain={gain_db:7.2f} dB (theory {theo_gain_db:7.2f}) | phase={ph_meas:7.1f}°")

    except KeyboardInterrupt:
        print("\n[sweep] interrupted by user, writing what we have...")
    finally:
        ar.close()
        es.close()

    # Write CSV
    out_path = args.out
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [
            "frequency_hz","vin_rms_v","vout_rms_v","gain_db_measured","phase_deg_measured","gain_db_theoretical","phase_deg_theoretical"
        ])
        w.writeheader()
        for r in rows:
            w.writerow(r)

    print(f"[sweep] wrote {len(rows)} rows → {out_path}")

    # Also make a nice plot (optional)
    if args.plot and rows:
        freq = np.array([r["frequency_hz"] for r in rows])
        gm = np.array([r["gain_db_measured"] for r in rows])
        gt = np.array([r["gain_db_theoretical"] for r in rows])

        plt.figure()
        plt.title("High-pass Filter Bode Magnitude")
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Gain (dB)")
        plt.semilogx(freq, gm, marker="o", label="Measured")
        plt.semilogx(freq, gt, marker="x", label="Theoretical")
        plt.grid(True, which="both")
        plt.legend()
        plt.tight_layout()
        plt.show()


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="mode", required=True)

    p_live = sub.add_parser("live")
    p_live.add_argument("--arduino", required=True, help="Arduino serial port, e.g. /dev/ttyUSB0")
    p_live.add_argument("--fs", type=float, default=2000.0, help="Sampling rate used in Arduino code (Hz)")
    p_live.add_argument("--nplot", type=int, default=600, help="Points shown in plot")
    p_live.add_argument("--fft", action="store_true", help="Show FFT window of output")
    p_live.set_defaults(func=mode_live)

    p_sw = sub.add_parser("sweep")
    p_sw.add_argument("--arduino", required=True, help="Arduino serial port, e.g. /dev/ttyUSB0")
    p_sw.add_argument("--esp32", required=True, help="ESP32 serial port, e.g. /dev/ttyUSB1")
    p_sw.add_argument("--fs", type=float, default=2000.0, help="Sampling rate used in Arduino code (Hz)")
    p_sw.add_argument("--nsamples", type=int, default=1024, help="Samples per frequency")
    p_sw.add_argument("--settle", type=float, default=0.25, help="Seconds to settle after changing frequency")
    p_sw.add_argument("--fstart", type=float, default=50.0)
    p_sw.add_argument("--fend", type=float, default=5000.0)
    p_sw.add_argument("--fstep", type=float, default=50.0)
    p_sw.add_argument("--out", default="results/measurements.csv")
    p_sw.add_argument("--plot", action="store_true", help="Plot measured vs theoretical gain")
    p_sw.set_defaults(func=mode_sweep)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
