"""
設定した台数全てのサーボを0どにする

picoのGPIO #7,8,9,10,11,12 pinにサーボを接続
servo_n = 6 で、接続しているサーボの台数を設定
        1台目が#7で順に増えていくこと
"""

from machine import Pin, PWM
import time

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
        

for angle in range(0, 181, 1):
    set_angle(angle)
    time.sleep(0.01)
print(angle)

for angle in range(180, -1, -1):
    set_angle(angle)
    time.sleep(0.01)
print(angle)

# --- PWM停止（必要なら） ---
for pwm in servo:
    pwm.deinit()