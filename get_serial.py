import os
import serial
import threading
from datetime import datetime
import time

# グローバル変数で書き込みデータを保持
write_data = ""

# ターミナルからの入力を処理するスレッド関数
def read_input():
    global write_data
    while True:
        write_data = input("Enter command: ")

def send_break_signal(ser):
    # ブレークシグナルを送信
    ser.send_break(duration=0.012)  # 12ms
    time.sleep(0.00833)  # 8.33ms のマークシグナル

def send_command(ser, command):
    # コマンドをフォーマットして送信
    full_command = f"{command}!".encode('ascii')
    ser.write(full_command)

def receive_and_save_serial_data(port_name, save_directory):
    global write_data
    try:
        with serial.Serial(port_name, baudrate=1200, bytesize=7, parity=serial.PARITY_EVEN, stopbits=1) as ser:
            ser.timeout = 1  # タイムアウトを1秒に設定
            current_date = datetime.now().strftime("%y%m%d")
            file_name = os.path.join(save_directory, f"{current_date}.log")

            send_break_signal(ser)  # ブレークシグナルを送信してセンサーを起動

            while True:
                incoming = ser.readline().decode('ascii').strip()  # 改行を取り除く
                if incoming:
                    # 日付が変わったかどうかを確認
                    new_date = datetime.now().strftime("%y%m%d")
                    if new_date != current_date:
                        current_date = new_date
                        file_name = os.path.join(save_directory, f"{current_date}.log")

                    with open(file_name, 'a') as serial_file:  # 'a'モードでファイルを開く
                        serial_file.write(incoming + '\n')  # 受信したデータをファイルに書き込む

                # 入力されたコマンドがあれば送信
                if write_data:
                    send_command(ser, write_data)  # SDI-12コマンドを送信
                    write_data = ""  # コマンドを送信したらクリア

    except KeyboardInterrupt:
        print("Program stopped by user.")
    except serial.SerialException:
        print("Error: Could not open serial port.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # 入力読み取りスレッドを開始
    input_thread = threading.Thread(target=read_input)
    input_thread.daemon = True  # メインプログラムが終了したらスレッドも終了させる
    input_thread.start()

    # シリアル通信関数を呼び出す
    receive_and_save_serial_data("COM3", "./data")
