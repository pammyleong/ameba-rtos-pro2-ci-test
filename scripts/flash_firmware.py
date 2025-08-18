#!/usr/bin/env python3
import subprocess
import platform
import argparse
import serial
import time
import sys

def main():
    print("Start flashing...")
    # 1. Create the argument parser
    parser = argparse.ArgumentParser(description="Auto Flash Tool Runner")

    # 2. Add arguments
    parser.add_argument('--image_exe', required=True, help='Path to Image Tool executable')
    parser.add_argument('--auto_flash_exe', required=True, help='Path to Auto_Flash executable')
    parser.add_argument('--uartfwburn_exe', required=True, help='Path to Flash FW executable')
    # parser.add_argument('--tools_path', required=True, help='Path to tools folder (e.g. .)')
    parser.add_argument('--com_port', required=True, help='COM port (e.g. /dev/ttyUSB0)')
    parser.add_argument('--baud_rate', type=int, required=True, help='Baud rate (e.g. 115200)')

    # 3. Parse arguments
    args = parser.parse_args()

    # 4. Detect OS and build the command
    # system_name = platform.system().lower()

    # if system_name == 'linux':
    #     cmd = [
    #         "./image_tool/Auto_Flash_Pro2_V3.3_linux",
    #         args.tools_path,
    #         args.com_port,
    #         str(args.baud_rate)
    #     ]
    # elif system_name == 'windows':
    #     cmd = [
    #         "./image_tool/Auto_Flash_Pro2_V3.3_win.exe",
    #         args.tools_path,
    #         args.com_port,
    #         str(args.baud_rate)
    #     ]
    # elif system_name == 'darwin':
    #     cmd = [
    #         "./image_tool/Auto_Flash_Pro2_V3.3_mac",
    #         args.tools_path,
    #         args.com_port,
    #         str(args.baud_rate)
    #     ]
    # else:
    #     raise RuntimeError(f"Unsupported OS: {system_name}")

    # 5. Print the exact shell command
    # print(" ".join(cmd))
    
    # parser = argparse.ArgumentParser(description="Flash Ameba firmware and check logs for faults.")
    # # parser.add_argument('--image_exe', required=True, help='Path to image executable')
    # # parser.add_argument('--tools_path', required=True, help='Path to tools folder')
    # parser.add_argument('--com_port', required=True, help='COM port')
    # #parser.add_argument('--board', required=True, help='Board name')
    # parser.add_argument('--baud_rate', default=115200, type=int, help='Baud rate for serial monitor (default: 115200)')
    # args = parser.parse_args()

    cmd = [
        args.image_exe,
        args.auto_flash_exe,
        args.com_port,
        str(args.baud_rate),
        "{board}",
        'Enable',
        'Disable',
        '2000000',
        args.uartfwburn_exe,
        "0x60000",
        "0x460000",
        "0x530000"
    ]
    print(cmd)
    # # # Build the exact command you want:
    # # cmd = [
    # #     args.image_exe,
    # #     args.tools_path,
    # #     args.com_port,
    # #     str(args.baud_rate),
    # # ]

    # # system_name = platform.system().lower()
    # # if system_name == 'windows':
    # #     cmd.extend([
    # #         'uartfwburn.exe',
    # #         'Auto_Flash_Pro2_V3.3_win.exe'
    # #     ])
    # # elif system_name == 'darwin':
    # #     cmd.extend([
    # #         'uartfwburn.darwin',
    # #         'Auto_Flash_Pro2_V3.3_mac'
    # #     ])
    # # elif system_name == 'linux':
    # #     cmd.extend([
    # #         'uartfwburn.linux',
    # #         'Auto_Flash_Pro2_V3.3_linux'
    # #     ])
    # # else:
    # #     raise RuntimeError(f"Unsupported OS: {system_name}")
    # system_name = platform.system().lower()

    # if system_name == 'linux':
    #     cmd = [
    #         "./image_tool/Auto_Flash_Pro2_V3.3_linux",
    #         ".",
    #         args.com_port,
    #         str(args.baud_rate)
    #     ]
    # elif system_name == 'windows':
    #     ...
    # elif system_name == 'darwin':
    #     ...
    # else:
    #     raise RuntimeError(f"Unsupported OS: {system_name}")
    # # cmd.extend([
    # #     '0x60000',
    # #     '0x460000',
    # #     '0x530000'
    # # ])

    # print(f"Running: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False
        )
    except Exception as e:
        print(f"Error running flash command: {e}")
        sys.exit(1)

    output = result.stdout
    print("--- Flashing log start ---")
    print(output)
    print("--- Flashing log end ---")

    if result.returncode != 0:
        print(f"Flashing tool returned non-zero exit code: {result.returncode}")
        sys.exit(result.returncode)

    if "Bus Fault" in output or "bus fault" in output.lower():
        print("Detected HardFault in flashing log. Marking as failure.")
        sys.exit(1)

    print("Flashing completed successfully with no hard fault detected.")

    # === Start serial monitor ===
    print(f"Opening serial port {args.com_port} at {args.baud_rate} baud...")
    try:
        ser = serial.Serial(args.com_port, args.baud_rate, timeout=1)
        time.sleep(2)  # Give MCU time to reset after flash
        print("--- Serial monitor --- (Press CTRL+C to stop)")

        while True:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if line:
                print(line)

    except KeyboardInterrupt:
        print("\nSerial monitor stopped by user.")

    except serial.SerialException as e:
        print(f"Serial error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()