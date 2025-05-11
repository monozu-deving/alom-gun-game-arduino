import serial
import time
import random
import pyttsx3

# COM 포트 번호는 장치 관리자에서 확인 (예: COM4)
ser = serial.Serial('COM4', 9600, timeout=1)
time.sleep(2)

tts = pyttsx3.init()
score = 0
slave_addresses = [8, 9, 10]

def send(cmd):
    ser.write((cmd + '\n').encode())

def recv():
    return ser.readline().decode().strip()

def set_target(slave, index):
    send(f"SET {slave} {index}")
    tts.say(f"타겟 {(slave - 8) * 4 + index + 1} 번입니다.")
    tts.runAndWait()

def check_hit():
    for addr in slave_addresses:
        send(f"GET {addr}")
        res = recv()
        if res.startswith("RESULT"):
            _, a, v = res.split()
            if int(v) == 1:
                return int(a)
    return None

while True:
    slave = random.choice(slave_addresses)
    index = random.randint(0, 3)
    correct_addr = slave

    set_target(slave, index)

    while True:
        time.sleep(0.2)
        hit = check_hit()
        if hit is None:
            continue
        if hit == correct_addr:
            score += 1
            print(f"✅ 정답! 점수: {score}")
            tts.say(f"정답입니다. 현재 점수는 {score}점입니다.")
            tts.runAndWait()
            break
        else:
            print("❌ 오답!")
            tts.say("오답입니다.")
            tts.runAndWait()
