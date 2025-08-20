#!/usr/bin/env python3
import subprocess
import platform
import argparse
import serial
import time
import sys
from serial.tools import miniterm

def main():
    print("Start flashing...")
    parser = argparse.ArgumentParser(description="Auto Flash Tool Runner")

    parser.add_argument('--image_exe', required=True, help='Path to Image Tool executable')
    parser.add_argument('--auto_flash_exe', required=True, help='Path to Auto_Flash executable')
    parser.add_argument('--tool_path', required=True, help='Path to tools executable')
    parser.add_argument('--uartfwburn_exe', required=True, help='Path to Flash FW executable')
    parser.add_argument('--com_port', required=True, help='COM port (e.g. /dev/ttyUSB0)')
    parser.add_argument('--baud_rate', type=int, required=True, help='Baud rate (e.g. 115200)')
    
    # For single-file burn:
    parser.add_argument('-f', '--bin', required=True, help='Binary to flash (e.g. flash_ntz.bin)')

    args = parser.parse_args()
    
    # --- Flash commands ---
    cmd1 = [
        args.auto_flash_exe,
        args.tool_path,
        args.com_port,
        str(args.baud_rate),
    ]
    print("Running:", " ".join(cmd1))
    try:
        result1 = subprocess.run(cmd1, text=True)
    except Exception as e:
        print(f"Error running flash command: {e}")
        sys.exit(1)

    if result1.returncode != 0:
        print(f"Flashing tool returned non-zero exit code: {result1.returncode}")
        sys.exit(result1.returncode)

    cmd2 = [
        args.uartfwburn_exe,
        "-p", args.com_port,
        "-f", args.bin,
        "-b", str(args.baud_rate),
        "-U",
        "-x", "32"
    ]
    print("Running:", " ".join(cmd2))
    try:
        result2 = subprocess.run(cmd2, text=True)
    except Exception as e:
        print(f"Error running flash command: {e}")
        sys.exit(1)

    if result2.returncode != 0:
        print(f"UART fwburn returned non-zero exit code: {result2.returncode}")
        sys.exit(result2.returncode)

    print("\n--- Image uploaded ---")
    
    # Create the serial instance first
    ser = serial.serial_for_url(args.com_port, baudrate=int(args.baud_rate))
    
    # Pass it into Miniterm
    mt = miniterm.Miniterm(
        ser,
        echo=False,
        eol='crlf',   # or 'cr' / 'lf' depending on your logs
        filters=[]
    )
    mt.exit_character = '\x1d'  # Ctrl-]
    mt.menu_character = '\x14'  # Ctrl-T
    mt.set_rx_encoding('utf-8')
    mt.set_tx_encoding('utf-8')

    print(f"\nOpening miniterm on {args.com_port} @ {args.baud_rate}")
    print("Press Ctrl-] to exit.\n")

    mt.start()
    mt.join()

    # cmd1 = [
    #     args.auto_flash_exe,
    #     args.tool_path,
    #     args.com_port,
    #     str(args.baud_rate),
    # ]
    
    # print("Running:", " ".join(cmd1))
    
    # try:
    #     result1 = subprocess.run(
    #         cmd1,
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.STDOUT,
    #         text=True,
    #         check=False
    #     )
    # except Exception as e:
    #     print(f"Error running flash command: {e}")
    #     sys.exit(1)

    # if result1.returncode != 0:
    #     print(f"Flashing tool returned non-zero exit code: {result1.returncode}")
    #     sys.exit(result1.returncode)
        
    # cmd2 = [
    # args.uartfwburn_exe,   # e.g. "./uartfwburn.linux"
    # "-p", args.com_port,   # e.g. "/dev/ttyUSB0"
    # "-f", args.bin,        # e.g. "flash_ntz.bin"
    # "-b", str(args.baud_rate),  # e.g. "2000000"
    # "-U",
    # "-x", "32"
    # ]
    # print("Running:", " ".join(cmd2))
    
    # process = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    # for line in process.stdout:
    #     print(line, end="")   # prints live
    # process.wait()
    
    # # try:
    # #     result2 = subprocess.run(
    # #         cmd2,
    # #         stdout=subprocess.PIPE,
    # #         stderr=subprocess.STDOUT,
    # #         text=True,
    # #         check=False
    # #     )
    # # except Exception as e:
    # #     print(f"Error running flash command: {e}")
    # #     sys.exit(1)
        
    # print("--- Image uploaded ---")

    # # if result2.returncode != 0:
    # #     print(f"Flashing tool returned non-zero exit code: {result2.returncode}")
    # #     sys.exit(result2.returncode)

    # # if "Bus Fault" in output or "bus fault" in output.lower():
    # #     print("Detected HardFault in flashing log. Marking as failure.")
    # #     sys.exit(1)

    # # print("Flashing completed successfully with no hard fault detected.")

    # # === Start serial monitor ===
    # # print(f"Opening serial port {args.com_port} at {args.baud_rate} baud...")
    # # try:
    # #     ser = serial.Serial(args.com_port, args.baud_rate, timeout=1)
    # #     time.sleep(2)  # Give MCU time to reset after flash
    # #     print("--- Serial monitor --- (Press CTRL+C to stop)")

    # #     while True:
    # #         line = ser.readline().decode('utf-8', errors='ignore').strip()
    # #         if line:
    # #             print(line)

    # # except KeyboardInterrupt:
    # #     print("\nSerial monitor stopped by user.")

    # # except serial.SerialException as e:
    # #     print(f"Serial error: {e}")
    # #     sys.exit(1)

if __name__ == '__main__':
    main()