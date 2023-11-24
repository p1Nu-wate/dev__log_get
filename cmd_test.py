import subprocess

cmd = 'ls'#<=ここにコマンドを当てはめる
process = (subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]).decode('utf-8')
print('コマンドの実行結果は\n'+process+'です')#何かしらの処理