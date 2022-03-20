# -*- coding:utf-8 -*-
# python 3.7

import pygame.midi as m
import serial
import time
import threading

# VRChatの現行のワールドログ
filename = 'C:\\Users\\(Windowsログインユーザー名)\\AppData\\LocalLow\\VRChat\\VRChat\\output_log_XX-XX-XX.txt'

#接続したいCOMポートを選択
comport = serial.Serial('COM1', baudrate=115200, parity=serial.PARITY_NONE)

m.init()
i_num = m.get_count()

for i in range(i_num):
	print(i)
	print(m.get_device_info(i))

# 直前のMIDIポート一覧から仮想デバイスのポート選択(自分の環境では「IAC Driver My Port」)のIDを確認して、その数値に変更してください
midiout = m.Output(3)

def log2com():

	flag = 0
	rev_buf =''
	enc_buf = ''

	with open(filename,'r',encoding='UTF-8') as f:
		while True:
			c = f.read(1)							# ファイルを1バイト読み込み
			if c != '':								# EOFではないとき
				if ((flag == 12) and (c == ']')) :
					flag = 0							# フラグクリア
					enc_buf = bytes.fromhex(rev_buf)	# 16進数をbyteにエンコード
					# print("[",end='')					# 標準出力 (改行なし) <- 表示が実行速度のボトルネックになるのでデバッグ用本運用はコメントアウト
					# print(enc_buf.decode(),end='')	# 標準出力 (改行なし) byteを文字列にデコード <- バイナリ転送時はエラーになるので注意！<- 表示が実行速度のボトルネックになるのでデバッグ用本運用はコメントアウト
					comport.write(enc_buf)				# シリアルポート出力
					# print("]OUTPUT")					# 標準出力 <- 表示が実行速度のボトルネックになるのでデバッグ用本運用はコメントアウト
					enc_buf =''							# バッッファクリア
					rev_buf =''							# バッッファクリア

				elif flag == 12:
					rev_buf = rev_buf + c				# 受信した1バイトを受信バッファに結合

				elif ((flag == 11) and (c == '[')) :
					flag = 12
				elif ((flag == 10) and (c == 'A')) :
					flag = 11
				elif ((flag == 9) and (c == 'T')) :
					flag = 10
				elif ((flag == 8) and (c == 'A')) :
					flag = 9
				elif ((flag == 7) and (c == 'D')) :
					flag = 8
				elif ((flag == 6) and (c == '_')) :
					flag = 7
				elif ((flag == 5) and (c == 'T')) :
					flag = 6
				elif ((flag == 4) and (c == 'U')) :
					flag = 5
				elif ((flag == 3) and (c == 'P')) :
					flag = 4
				elif ((flag == 2) and (c == 'T')) :
					flag = 3
				elif ((flag == 1) and (c == 'U')) :
					flag = 2
				elif ((flag == 0) and (c == 'O')) :
					flag = 1
				else :
					flag = 0

def com2midi():

	while True:
		send_buf = comport.read(1)						# シリアルポートから1バイト受信(待ち)

		# 1byteのデータをMIDIに変換
		send_buf_value = ord(send_buf)					# 1バイトのバイナリを整数に変換(0-255)
		send_num = send_buf_value % 128					# 8bitの整数0-255を7bit(0-127)と1bitに分離 ( % で余り)
		send_vel = send_buf_value // 128				# 8bitの整数0-255を7bit(0-127)と1bitに分離 ( // で整数の商)

		# MIDIを発行
		midiout.note_on(send_num, send_vel, 1)			# MIDIを発行 (numver , vel , ch)
		# print("SEND [",1,"] : ",send_num,send_vel)	# 発行したMIDIの確認表示 <- 表示が実行速度のボトルネックになるのでデバッグ用本運用はコメントアウト

		# time.sleep(0.001)								# 1msecのスリープで1000byte/secの制限(8000bps) <- 受信待ち時間に引っ張られるので特に明示的なsleepはなくて問題なし

	midiout.close()
	m.quit()


thread1 = threading.Thread(target=log2com)
thread2 = threading.Thread(target=com2midi)
thread1.start()
thread2.start()

thread1.join()
thread2.join()

comport.close()
exit()
