# UdonSerial - うどんシリアル

VRChatのワールドとローカルPCのシリアルポートとの間で、シリアル通信をするためのコードです。

VRChat側へデータ入力はMIDI、VRChatからのデータ出力はoutputlogを使用しており、中継するソフトウェア(python)で、シリアルポートからMIDIへのデータ変換と、outputlogからシリアルポートへのデータ変換を行います。

- UdonSerial : VRChatのワールド用のUnity用のアセット
- com2vrchat : ゲートウェイソフトウェア(python)

なお、MIDIをループバックするために、仮想MIDIドライバ (loopMIDI)を使用します。
https://www.tobias-erichsen.de/software/loopmidi.html

全体図

# MIDIデータ仕様



# OutputLog書式


# pythonコードの使い方

~~~
# VRChatの現行のワールドログ
filename = 'C:\\Users\\hirokazu\\AppData\\LocalLow\\VRChat\\VRChat\\output_log_23-25-06.txt'
~~~

この部分を現在、joinしているVRChatログのパスに書き換えます

~~~
# 接続したいCOMポートを選択
comport = serial.Serial('COM9', baudrate=9600, parity=serial.PARITY_NONE)
~~~

この部分を、使用したいシリアルポートのCOM番号に書き換えます。

~~~
# 直前のMIDIポート一覧から仮想デバイスのポート(自分の環境では「IAC Driver My Port」)のIDを確認して、その数値にしてください
midiout = m.Output(3)
~~~

お使いの環境に合わせて、Loop MIDIの入力ポートの番号を設定します。

開発環境 : python 3.7 on Visual Studio 2019

# UdonSerialの実装 (Arduinoライク)

関数一覧 (関数の詳細はUdon SerialのReadme.mdにて)
- Serial_write(byte send_data)
- Serial_print(string send_data)
- Serial_println(string send_data)
- bool Serial_available() 
- byte Serial_read()
- byte Serial_peek()
- void Serial_flush()
- void setup()
- void loop()