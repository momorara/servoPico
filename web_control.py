"""
2023/06/16  PicoWでwebサーバーを立てて、webでボタンを押すと
            サンプルプログラムであり、セキュリティ、障害耐性など考慮されていません。
    01      picoのLEDが点灯、消灯します。
            thonnyに繋いだ状態で動作させてstopした後は、再接続してださい。
            多分ソケットのエラーを回復するのに30秒だかかかるっぽい
2023/06/17  ボタンを横に並べて、大きく。endボタン追加
v1.0
2026/05/11  servoPico用に改造
                SSD1306を削除
                BMP1280を削除
2026/05/12  よりDemoらしく改修
"""
import machine
from machine import Pin, PWM
import math
import random
import socket
import time
import network
import sys
import lib_AHT10
import config


# picoのGPIO #7,8,9,10,11,12 pinにサーボを設定
servo = [0,1,2,3,4,5]
for i in range(6):
    servo[i] = PWM(Pin(i+7))
    servo[i].freq(50)
# サーボの台数
servo_n = 6

def set_angle(angle):
    # 0〜180度 → duty変換
    duty = int(1638 + (angle / 180) * (8192 - 1638))
    for i in range(servo_n):
        servo[i].duty_u16(duty)

# --- 角度設定 ---
def set_angle1(pwm, angle):
    duty = int(1638 + (angle / 180) * 6553)  # 0.5ms〜2.5ms
    pwm.duty_u16(duty)

# エラーが2回続けば、データ欠損として、Noneとする。
def keisoku():
    try:
        temp1,humi1 = lib_AHT10.aht10(1)
        time.sleep(1)
    except:
        time.sleep(3)
        try:
            temp1,humi1 = lib_AHT10.aht10(1)
        except:
            temp1,humi1 = None,None

    # temp,press1 = lib_BMP1280.BMP()

    return temp1,humi1

# センサからデータを読み取る関数（具体的なセンサに合わせて修正が必要）
def read_sensor():
    # センサー測定
    temp,humi = keisoku()
    return temp, humi

# wifi設定値取得
SSID,PASSWORD = config.ID_PASS()
# ネットワーク設定
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(SSID, PASSWORD)  # Wi-FiのSSIDとパスワードを入力

# ネットワーク接続を待つ
while not sta_if.isconnected():
    print('Connecting to network...')
    time.sleep(1)
print('connected!')

# OLEDにipアドレス表示
status = sta_if.ifconfig()
print( 'ip = ' + status[0] )
# SSD1306.OLED_mes(status[0])

# GPIOピンの設定
led1 = machine.Pin(16, machine.Pin.OUT)
led2 = machine.Pin(17, machine.Pin.OUT)

led1.on()
time.sleep(2)
led1.off()
led2.on()
time.sleep(2)
led2.off()

# HTMLページの設定
html = """<!DOCTYPE html>
<html>
    <head> 
        <title>RaspberryPi Pico LED Control</title> 
        <style>
            .button {{
                font-size: 20px;
                padding: 10px 24px;
                margin: 24px 2px;  /* ボタン間のスペースを広げる */
                display: inline-block;
                border: none;
                color: black;  /* テキスト色を黒に設定 */
                text-align: center;
                text-decoration: none;
                transition-duration: 0.4s;
                cursor: pointer;
                border-radius: 12px;
                box-shadow: 0 9px #999;
            }}
            .button:active {{
                box-shadow: 0 5px #666;
                transform: translateY(4px);
            }}
            .button1 {{
                background-color: #4CAF50;
            }}
            .button2 {{
                background-color: #008CBA;
            }}
            .button3 {{
                background-color: #f44336;
            }}
            .button4 {{
                background-color: #e7e7e7; 
                color: black; 
            }}
            .reading {{
                font-size: 30px;  /* テキストサイズを大きく設定 */
            }}
        </style>
    </head>
    <body> 
        <h1>RaspberryPi Pico LED + Servo Control and Sensor</h1> 
        <form method="POST">
            <button class="button" name="led" value="ON1">servo 0</button>
            <button class="button" name="led" value="OFF1">servo 90</button>
            <button class="button" name="led" value="ON2">servo 180</button>
            <button class="button" name="led" value="OFF2">servo 180 -> 90 -> 0</button><br/>

            <button class="button" name="led" value="BLINK">BLINK</button>
            <button class="button" name="led" value="END">DEMO</button>
        </form>
        <p style="font-size: 30px;">Temperature: {temp} C</p>
        <p style="font-size: 30px;">Humidity   : {humi} %</p>
    </body>
</html>
"""
def web_page(temp, humi):
  return html.format(temp=temp, humi=humi)
# def web_page():
#     return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
print('start')
print('-----')

while True:
    conn, addr = s.accept()
    request = conn.recv(1024)
    request = str(request)
    led_on1 = request.find('led=ON1')
    led_off1 = request.find('led=OFF1')
    led_on2 = request.find('led=ON2')
    led_off2 = request.find('led=OFF2')
    led_blink = request.find('led=BLINK')
    led_end = request.find('led=END')

    # print(led_on1,led_off1,led_on2,led_off2)


    # センサからデータを読み取る
    temp, humi = read_sensor()

    if led_on1 > 6:
        print('servo 0')
        led1.on()
        for angle in range(180, -1, -1):
            set_angle(angle)
            time.sleep(0.01)
        led1.off()

    if led_off1 > 6:
        print('servo 90')
        led1.on()
        for angle in range(0, 90, 1):
            set_angle(angle)
            time.sleep(0.01)
        led1.off()

    if led_on2 > 6:
        print('servo 180')
        led1.on()
        for angle in range(0, 181, 1):
            set_angle(angle)
            time.sleep(0.01)
        led1.off()

    if led_off2 > 6:
        print('servo 180-90-0')
        led1.on()
        led2.on()
        for angle in range(0, 90, 1):
            set_angle(angle)
            time.sleep(0.01)
        time.sleep(2)
        for angle in range(90, 181, 1):
            set_angle(angle)
            time.sleep(0.01)
        time.sleep(2)
        for angle in range(180, -1, -1):
            set_angle(angle)
            time.sleep(0.01)
        led2.off()
        led1.off()

    if led_blink > 6:
        print('LED BLINK')
        for i in range(5):
            led1.on()
            time.sleep(0.5)
            led1.off()
            led2.on()
            time.sleep(0.5)
            led2.off()
            led2.off()

    if led_end > 6:
        print('DEMO')
        duration=8

        # 0に戻す
        angle=0
        for pwm in servo:
            set_angle1(pwm,angle)
            time.sleep(0.2)

        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
            for pwm in servo:
                angle = random.randint(60, 120)
                set_angle1(pwm, angle)
            time.sleep(0.3)
    
        start = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
            t = time.ticks_ms() / 1000
            base = 90 + 30 * math.sin(t)
            for pwm in servo:
                set_angle1(pwm, base)
            time.sleep(0.02)

        # 0に戻す
        angle=0
        for pwm in servo:
            set_angle1(pwm,angle)
            time.sleep(0.2)

    response = web_page(temp, humi)
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
