import os
import serial
from datetime import datetime

def receive_and_save_serial_data(port_name="COM1", timeout=10, save_directory="./data"):
    try:
        with serial.Serial(port_name, timeout=timeout) as ser:
            return_str = ""
            while True:
                incoming = ser.readline().decode('utf-8')
                if not incoming:
                    break
                print(f"Received: {incoming}")  # データをターミナルに表示
                return_str += incoming

            # シリアルデータをファイルに保存
            timestamp = datetime.now().strftime("%y%m%d%H%M%S")
            file_name = os.path.join(save_directory, f"{timestamp}.log")
            with open(file_name, 'w') as serial_file:
                serial_file.write(return_str)

            return return_str
    except serial.SerialTimeoutException:
        return "Error: Serial Port read timed out."
    except Exception as e:
        return f"Error: {e}"