
from machine import Pin, PWM
import time
import math
import random

# --- PWM初期化 ---
pins = [7,8,9,10,11,12]
servos = []

for p in pins:
    pwm = PWM(Pin(p))
    pwm.freq(50)
    servos.append(pwm)

# --- 角度設定 ---
def set_angle(pwm, angle):
    duty = int(1638 + (angle / 180) * 6553)  # 0.5ms〜2.5ms
    pwm.duty_u16(duty)

# --- パターン① 波 ---
def wave_motion(duration=5):
    print("▶ パターン① 波の動き 開始")
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
        t = time.ticks_ms() / 1000
        for i, pwm in enumerate(servos):
            angle = 90 + 40 * math.sin(t * 2 + i)
            set_angle(pwm, angle)
        time.sleep(0.02)
    print("▶ パターン① 終了\n")

# --- パターン② ランダム ---
def random_motion(duration=5):
    print("▶ パターン② ランダム動作 開始")
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
        for pwm in servos:
            angle = random.randint(60, 120)
            set_angle(pwm, angle)
        time.sleep(0.3)
    print("▶ パターン② 終了\n")

# --- パターン③ スキャン ---
def scan_motion():
    print("▶ パターン③ スキャン動作 開始")
    for pwm in servos:
        set_angle(pwm, 40)
        time.sleep(0.1)
        set_angle(pwm, 140)
    print("▶ パターン③ 終了\n")

# --- パターン④ 呼吸 ---
def breathing_motion(duration=5):
    print("▶ パターン④ 呼吸動作 開始")
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < duration * 1000:
        t = time.ticks_ms() / 1000
        base = 90 + 30 * math.sin(t)
        for pwm in servos:
            set_angle(pwm, base)
        time.sleep(0.02)
    print("▶ パターン④ 終了\n")

# --- メイン ---
print("=== サーボ動作スタート ===\n")

wave_motion()
random_motion()
scan_motion()
breathing_motion()

# 0に戻す
angle=0
for pwm in servos:
    set_angle(pwm,angle)
    time.sleep(0.2)

print("=== すべての動作終了 ===")

# --- PWM停止（必要なら） ---
for pwm in servos:
    pwm.deinit()