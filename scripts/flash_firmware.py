#!/usr/bin/env python3
import subprocess
import platform
import argparse
import serial
import time
import sys

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

if __name__ == '__main__':
    main()