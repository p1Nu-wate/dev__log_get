import os
import re
import csv

# 指定ディレクトリ内の.logファイルを検索する関数
def find_log_files(directory):
    log_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".log"):
                log_files.append(os.path.join(root, file))
    # print(log_files)
    return log_files

# ログファイルから必要な情報を抽出する関数
def extract_log_info(log_file):
    log_info = []
    with open(log_file, 'r') as file:
        lines = file.readlines()
        date = None
        for i, line in enumerate(lines):
            # 日付のフォーマットを修正する (月/日/年 -> 年/月/日)
            date_match = re.match(r'(\d{2})/(\d{2})/(\d{2}) (\d{2}:\d{2}:\d{2})', line.strip())
            if date_match:
                mm, dd, yy, time = date_match.groups()
                date = f"20{yy}/{mm}/{dd} {time}"
                # print("Found date:", date)

            # 'AVERAGE NOISE LEVEL' の行を大文字小文字を区別せずに検索
            if re.search(r'average noise level \(-dbm per time interval\):', line, re.IGNORECASE):
                if date:
                    # ノイズレベルの値を抽出する
                    noise_values = [int(val) for val in re.findall(r'-?\d+', lines[i + 2])]
                    log_info.append((date, noise_values))
    # print(log_info)
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
    log_directory = "./log_Indonesia/remote/201705"  # ログファイルが格納されているディレクトリを指定してください
    output_csv_file = "./export/Indonesia_1705/remote/output_0.csv"  # 出力するCSVファイル名を指定してください

    log_files = find_log_files(log_directory)
    log_info = []

    for log_file in log_files:
        log_info.extend(extract_log_info(log_file))

    # print(log_info)
    if log_info:
        write_csv(output_csv_file, log_info)
        print("CSVファイルにデータを出力しました。")
    else:
        print("ログ情報が見つかりませんでした。")