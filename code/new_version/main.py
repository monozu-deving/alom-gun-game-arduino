import random
import serial
import time
from dearpygui import dearpygui as dpg

button_ser = serial.Serial('COM6', 9600, timeout=0.1)
relay_ser = serial.Serial('COM7', 9600, timeout=0.1)

CELL_WIDTH = 150
CELL_HEIGHT = 150
GRID_COLS = 3
GRID_ROWS = 4
current_target = random.randint(1, 12)
score = 0
message = "🎯 버튼을 눌러 시작하세요"

def set_target(target):
    # 10,11,12은 'a','b','c'
    cmd = str(target) if target < 10 else chr(ord('a') + target - 10)
    relay_ser.write('5'.encode())
    dpg.set_value("target_text", f"🎯 대상: {target}")

def draw_grid():
    dpg.delete_item("canvas", children_only=True)
    for i in range(12):
        row = i // GRID_COLS
        col = i % GRID_COLS
        x = col * CELL_WIDTH
        y = row * CELL_HEIGHT
        dpg.draw_rectangle((x, y), (x + CELL_WIDTH, y + CELL_HEIGHT), color=(70,70,70,255), parent="canvas")
        dpg.draw_text((x + 10, y + 10), text=str(i+1), size=20, color=(255,255,255,255), parent="canvas")
    row = (current_target - 1) // GRID_COLS
    col = (current_target - 1) % GRID_COLS
    cx = col * CELL_WIDTH + CELL_WIDTH // 2
    cy = row * CELL_HEIGHT + CELL_HEIGHT // 2
    dpg.draw_circle((cx, cy), 30, fill=(0,255,0,150), parent="canvas")

def check_hit():
    global score, current_target, message
    try:
        line = button_ser.readline().decode(errors='ignore').strip()
        if line.isdigit():
            val = int(line)
            if val == current_target:
                score += 1
                message = f"✅ 정답! 버튼 {val}"
                dpg.set_value("score_text", f"🏆 점수: {score}")
                current_target = random.randint(1, 12)
                set_target(current_target)
                draw_grid()
            else:
                message = f"❌ 오답: {val} (기대: {current_target})"
        dpg.set_value("message_text", message)
    except:
        pass

dpg.create_context()
with dpg.window(label="UFO Grid Game", tag="main"):
    dpg.add_text(f"🎯 대상: {current_target}", tag="target_text")
    dpg.add_text(f"🏆 점수: 0", tag="score_text")
    dpg.add_text(message, tag="message_text")
    with dpg.drawlist(width=GRID_COLS * CELL_WIDTH, height=GRID_ROWS * CELL_HEIGHT, tag="canvas"):
        pass

draw_grid()
set_target(current_target)

with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=lambda: None)

dpg.create_viewport(title="Gun Game", width=600, height=700)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)

while dpg.is_dearpygui_running():
    check_hit()
    dpg.render_dearpygui_frame()
    time.sleep(0.05)

dpg.destroy_context()
