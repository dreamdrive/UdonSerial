
using System;
using UdonSharp;
using UnityEngine;
using VRC.SDKBase;
using VRC.Udon;

public class RealSerial : UdonSharpBehaviour
{

    // 受信用のリングバッファ(1kbyte)
    private byte[] buffer_data = new byte[1024];
    private int write_index = 0;
    private int read_index = 0;

    void Start()
    {
        Serial_println("Start! Serial");
    }

    void Update()
    {
        loop();
    }

    public override void MidiNoteOn(int channel, int number, int velocity)
    {
        int rev_number;
        rev_number = number + (velocity * 128);
        buffer_data[write_index] = (byte)rev_number;
        write_index++;
        if (write_index == 1024) write_index = 0;
    }

    private void Serial_write(byte send_data)
    {
        Debug.Log("OUTPUT_DATA[" + string.Format("{0:X2}", send_data) + "]");
        // 1バイトを16進数表示にしてログに出力
    }

    private void Serial_print(string send_data)
    {
        char[] values = send_data.ToCharArray();

        string output_data;
        output_data = "OUTPUT_DATA[";

        // 文字を1文字ずつ16進数のStringに変換する
        foreach (char letter in values)
        {
            int value = Convert.ToInt32(letter);
            output_data = output_data + string.Format("{0:X2}", value);
        }

        // 改行なしの場合は最後が"]"
        output_data = output_data + "]";

        Debug.Log(output_data);
        // 1バイトを16進数表示にしてログに出力
    }

    private void Serial_println(string send_data)
    {
        char[] values = send_data.ToCharArray();

        string output_data;
        output_data = "OUTPUT_DATA[";

        // 文字を1文字ずつ16進数のStringに変換する
        foreach (char letter in values)
        {
            int value = Convert.ToInt32(letter);
            output_data = output_data + string.Format("{0:X2}", value);
        }

        // 改行ありの場合は最後が"]"
        output_data = output_data + "]";

        Debug.Log(output_data);
        // 1バイトを16進数表示にしてログに出力
    }

    private bool Serial_available() {
        if (write_index == read_index) return false;   // 処理すべきバッファがない
        else return true;                              // 処理すべきバッファがある
    }

    private byte Serial_read() {
        byte rev_data;

        if (write_index == read_index) return 0;   // 処理すべきバッファがない(とりあえず0を返す)
        rev_data = buffer_data[read_index];

        read_index++;
        if (read_index == 1024) read_index = 0;

        return rev_data;
    }

    private byte Serial_peek()
    {
        byte rev_data;

        if (write_index == read_index) return 0;   // 処理すべきバッファがない(とりあえず0を返す)
        rev_data = buffer_data[read_index];

        // peek関数は読み取り位置を移動しない

        return rev_data;
    }

    private void Serial_flush()
    {
        // 受信バッファをクリア(インデックスを同じ値に)
        read_index = write_index;
    }

    private void loop(){

        byte key;

        // 受信データがあった時だけ、処理を行う
        if (Serial_available())             // 受信データがあるか？
        {       
            key = Serial_read();            // 1バイトだけバッファに受信
            Serial_write(key);              // 受信したデータを送り返す

        }
    }
}
