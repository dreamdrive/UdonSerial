# -*- coding:utf-8 -*-
# python 3.7

import pygame.midi as m
import serial
import time
import threading

# VRChatの現行のワールドログ
filename = 'C:\\Users\\hirokazu\\AppData\\LocalLow\\VRChat\\VRChat\\output_log_23-25-06.txt'

#接続したいCOMポートを選択
comport = serial.Serial('COM9', baudrate=9600, parity=serial.PARITY_NONE)

m.init()
i_num = m.get_count()

for i in range(i_num):
	print(i)
	print(m.get_device_info(i))

# 直前のMIDIポート一覧から仮想デバイスのポート(自分の環境では「IAC Driver My Port」)のIDを確認して、その数値にしてください
midiout = m.Output(3)

def log2com():
	flag = 0
	rev_buf =''
	enc_buf = ''
	with open(filename,'r',encoding='UTF-8') as f:
		# f.seek(-1000, 2)
		while True:
			c = f.read(1)							# 1バイト読み込み
			if c != '':								# EOFではないとき
				if ((flag == 12) and (c == ']')) :
					flag = 0							# フラグクリア
					enc_buf = bytes.fromhex(rev_buf)	# 16進数をbyteにエンコード
					print("[",end='')					# 標準ファクリア
					# print(enc_buf.decode(),end='')		# 標準出力(改行なし) byteを文字列にデコード
					comport.write(enc_buf)				# シリアルポート出力
					print("]OUTPUT")					# 標準ファクリア
					enc_buf =''							# バ出力
					rev_buf =''							# バッッファクリア

				elif ((flag == 12) and (c == '}')) :
					flag = 0							# フラグクリア
					enc_buf = bytes.fromhex(rev_buf)	# 16進数をbyteにエンコード
					print("[",end='')					# 標準ファクリア
					print(enc_buf.decode(),end='')		# 標準出力(改行なし) byteを文字列にデコード
					comport.write(enc_buf)				# シリアルポート出力
					print("<CRLF>]OUTPUT")				# 標準ファクリア
					comport.write("\n\r".encode())		# シリアルポート出力(改行コード)
					rev_buf =''							# バッファクリア
					enc_buf =''							# バッファクリア

				elif flag == 12:
				   # print(c, end='')	# 改行なし標準出力
				   # comport.write(c.encode()) # COMポート出力
					rev_buf = rev_buf + c				# 受信した1文字結合

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
		send_buf = comport.read(1)
		send_buf_value = ord(send_buf)

		# // で整数の商
		# %で余り
		send_num = send_buf_value % 128
		send_vel = send_buf_value // 128

		# numver , vel , ch
		midiout.note_on(send_num, send_vel, 1)
		print("SEND [",1,"] : ",send_num,send_vel)

		time.sleep(0.002)

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
