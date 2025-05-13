import random
import serial
import time
from dearpygui import dearpygui as dpg

# 시리얼 포트 연결
ser = serial.Serial('COM7', 9600, timeout=0.1)

CELL_WIDTH = 150
CELL_HEIGHT = 150
GRID_COLS = 3
GRID_ROWS = 4

current_target = random.randint(1, 12)
score = 0

def update_target():
    global current_target
    current_target = random.randint(1, 12)
    dpg.set_value("target_text", f"🎯 대상: {current_target}")
    slave = (current_target - 1) // 4 + 8
    index = (current_target - 1) % 4
    ser.write(f"SET {slave} {index}\n".encode())

def draw_grid():
    dpg.delete_item("canvas", children_only=True)
    for i in range(12):
        row = i // GRID_COLS
        col = i % GRID_COLS
        x = col * CELL_WIDTH
        y = row * CELL_HEIGHT
        dpg.draw_rectangle((x, y), (x + CELL_WIDTH, y + CELL_HEIGHT), color=(70, 70, 70, 255), parent="canvas")
        dpg.draw_text((x + 10, y + 10), text=str(i + 1), size=20, color=(255, 255, 255, 255), parent="canvas")
    
    # 타겟 표시
    row = (current_target - 1) // GRID_COLS
    col = (current_target - 1) % GRID_COLS
    cx = col * CELL_WIDTH + CELL_WIDTH // 2
    cy = row * CELL_HEIGHT + CELL_HEIGHT // 2
    dpg.draw_circle((cx, cy), 30, fill=(0, 255, 0, 150), parent="canvas")

def check_hit():
    global score
    try:
        line = ser.readline().decode(errors='ignore').strip()
        if line.isdigit():
            pressed = int(line)
            dpg.set_value("pressed_text", f"👆 누른 버튼: {pressed}")
            print(f"누른 버튼: {pressed}")
            if pressed == current_target:
                score += 1
                dpg.set_value("score_text", f"🏆 점수: {score}")
                update_target()
                draw_grid()
    except:
        pass

# GUI 초기화
dpg.create_context()
with dpg.window(label="건슈팅 게임", tag="main"):
    dpg.add_text(f"🎯 대상: {current_target}", tag="target_text")
    dpg.add_text("👆 누른 버튼: -", tag="pressed_text")
    dpg.add_text("🏆 점수: 0", tag="score_text")
    with dpg.drawlist(width=GRID_COLS * CELL_WIDTH, height=GRID_ROWS * CELL_HEIGHT, tag="canvas"):
        pass

draw_grid()

# 기본 GUI 핸들러 등록
with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=lambda: None)

dpg.create_viewport(title="Gun Game", width=600, height=700)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main", True)

# 루프 처리
while dpg.is_dearpygui_running():
    check_hit()
    dpg.render_dearpygui_frame()
    time.sleep(0.05)

dpg.destroy_context()
