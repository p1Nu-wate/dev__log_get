import os
import re
import csv
from datetime import datetime

# 指定ディレクトリ内の.logファイルを検索する関数
def find_log_files(directory):
    log_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".log"):
                log_files.append(os.path.join(root, file))
    return log_files

# ログファイルから必要な情報を抽出する関数
def extract_log_info(log_file):
    log_info = []
    with open(log_file, 'r') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            if re.search(r'AVERAGE NOISE LEVEL \(- DB PER TIME INTERVAL\):', line):
                # 日付の行を探索
                for j in range(i - 1, -1, -1):
                    if re.match(r'\d{2}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}', lines[j].strip()):
                        date = lines[j].strip()
                        break
                noise_values = [int(val) for val in lines[i + 2].split()]
                log_info.append((date, noise_values))
    return log_info

# CSVファイルにデータを書き込む関数
def write_csv(output_file, log_info):
    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Date', '0-5', '5-10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60', 'AVE'])
        for date, noise_values in log_info:
            row = [date] + noise_values
            csv_writer.writerow(row)

if __name__ == "__main__":
    log_directory = "./log/"  # ログファイルが格納されているディレクトリを指定してください
    output_csv_file = "./export/output_12.csv"  # 出力するCSVファイル名を指定してください

    log_files = find_log_files(log_directory)
    log_info = []

    for log_file in log_files:
        log_info.extend(extract_log_info(log_file))

    if log_info:
        write_csv(output_csv_file, log_info)
        print("CSVファイルにデータを出力しました。")
    else:
        print("ログ情報が見つかりませんでした。")