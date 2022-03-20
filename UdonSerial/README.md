# UdonSerialのサンプル関数について

Udon Serial Echoのサンプルワールドに用意した、Arduinoライクな関数群の紹介です。

## 関数一覧

|  関数名  |  機能  |  引数  |  戻り値  |
| ---- | ---- | ---- | ---- |
|  Serial_write(byte send_data)  |  シリアルポートに1byte送信  | byte型 | ---- |
|  Serial_print(string send_data)  |  シリアルポートに文字列送信  | String型 | ---- |
|  Serial_println(string send_data)  |  文字列送信(改行付き)  | ---- | ---- |
|  Serial_available()  |  受信バッファに未処理のデータがあるかどうか  | ---- | bool型 |
|  Serial_read()  |  1byteデータ受信  | ---- | byte型 |
|  Serial_peek()  |  1byteデータ受信(リングバッファのインデックスを進めない)  | ---- | byte型 |
|  Serial_flush()  |  受信バッファクリア(未処理のデータを破棄する)  | ---- | ---- |
|  setup()  |  world読み込み時に一度だけ呼ばれる関数 (UnityのStart関数から呼ばれる)  | ---- | ---- |
|  loop()  |  毎フレーム呼ばれる関数 (UnityのUpdate関数から呼ばれる)  | ---- | ---- |

## Udon Serialの仕様

- MIDIを通じて受信したデータは一度、Udon内のバッファ(リングバッファ)に保管されます。
- バッファは、1024byte用意しています。
- 未処理のデータが1024byteを超えるとオーバーフローしてしまうため、未処理のデータが1024byte分破棄されます。

## Udon Serial(全体像)について

こちらの[Readme.md](./../README.md)をお読みください


# 履歴
2022/03/20 : とりあえず、リリース

# Author
- Micchy  
http://dream-drive.net  
https://twitter.com/Dream_Drive

なにかUdon Serialを拡張して楽しいネタ、これを利用して何か連動させたい案件などありましたら、趣味・お仕事問わず、ご連絡いただけましたら対応させていただきます。

# License
This is under MIT License.