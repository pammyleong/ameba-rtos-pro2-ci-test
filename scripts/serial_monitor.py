import subprocess, sys, time, serial
import platform
import argparse

def run_and_stream(cmd):
    print("Running:", " ".join(cmd), flush=True)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for line in p.stdout:
        print(line, end="", flush=True)
    rc = p.wait()
    if rc != 0:
        print(f"Command failed with exit code {rc}", flush=True)
        sys.exit(rc)

def serial_logger(port, baud, duration=10):
    ser = serial.Serial(port, baudrate=int(baud), timeout=0.2)
    end = time.time() + duration
    try:
        print("\n--- Image uploaded ---", flush=True)
        print(f"Tailing {port} @ {baud} for {duration}s...\n", flush=True)
        while time.time() < end:
            line = ser.readline()
            if line:
                print(line.decode("utf-8", errors="replace"), end="", flush=True)
    finally:
        ser.close()

def main():
    
    print("Opening Serial Monitor...")
    parser = argparse.ArgumentParser(description="Auto Flash Tool Runner")

    parser.add_argument('--com_port', required=True, help='COM port (e.g. /dev/ttyUSB0)')
    parser.add_argument('--baud_rate', type=int, required=True, help='Baud rate (e.g. 115200)')

    args = parser.parse_args()
    # comport = "COM5"
    # baudrate = "115200"
    serial_logger(args.com_port, str(args.baud_rate), duration=30)

if __name__ == "__main__":
    main()
