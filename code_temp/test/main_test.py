import random
import serial
import time
from dearpygui import dearpygui as dpg

# 시리얼 포트 설정
ser = serial.Serial('COM7', 9600, timeout=0.1)
time.sleep(2)

CELL_WIDTH = 150
CELL_HEIGHT = 150
GRID_COLS = 3
GRID_ROWS = 4
slave_addresses = [8, 9, 10]
target_button = random.randint(1, 12)
last_hit = None
score = 0

# 🎯 버튼 이벤트 처리 함수
def read_hit():
    line = ser.readline().decode().strip()
    if line.startswith("HIT"):
        try:
            _, addr, btn = line.split()
            addr = int(addr)
            btn = int(btn)
            return (addr - 8) * 4 + btn + 1
        except ValueError:
            return None
    return None

# 🟩 타겟 위치 표시
def update_grid():
    dpg.delete_item("ufo_canvas", children_only=True)
    for i in range(12):
        row = i // GRID_COLS
        col = i % GRID_COLS
        x = col * CELL_WIDTH
        y = row * CELL_HEIGHT
        dpg.draw_rectangle((x, y), (x + CELL_WIDTH, y + CELL_HEIGHT), color=(70, 70, 70, 255), parent="ufo_canvas")
        dpg.draw_text((x + 10, y + 10), text=str(i + 1), size=20, color=(255, 255, 255, 255), parent="ufo_canvas")

    # 🎯 타겟 그리기
    row = (target_button - 1) // GRID_COLS
    col = (target_button - 1) % GRID_COLS
    x = col * CELL_WIDTH + CELL_WIDTH // 2
    y = row * CELL_HEIGHT + CELL_HEIGHT // 2
    dpg.draw_circle((x, y), 30, color=(200, 200, 200, 255), fill=(0, 255, 0, 150), parent="ufo_canvas")

# 🌀 검사 및 결과 표시
def check_loop():
    global target_button, last_hit, score
    hit = read_hit()
    if hit is not None and hit != last_hit:
        last_hit = hit
        if hit == target_button:
            score += 1
            print(f"✅ 정답! 버튼 {hit} 눌림 | 점수: {score}")
            dpg.set_value("status", f"Answer! Button {hit} press")
            dpg.set_value("score", f"Score: {score}")
            target_button = random.randint(1, 12)
            update_grid()
        else:
            print(f"❌ 오답: 버튼 {hit} 눌림 (기대: {target_button}) | 점수: {score}")
            dpg.set_value("status", f"Wrong: Button {hit} press (Hope: {target_button})")

# 🪐 DearPyGui 시작
dpg.create_context()

with dpg.window(label="UFO Grid Game", tag="main_window"):
    dpg.add_text(f"Hope Button: {target_button}", tag="status")
    dpg.add_text(f"Score: {score}", tag="score")
    with dpg.drawlist(width=GRID_COLS * CELL_WIDTH, height=GRID_ROWS * CELL_HEIGHT, tag="ufo_canvas"):
        pass

update_grid()

with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=lambda: None)

dpg.create_viewport(title="UFO Grid Game", width=600, height=750)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)

while dpg.is_dearpygui_running():
    check_loop()
    dpg.render_dearpygui_frame()
    time.sleep(0.1)

dpg.destroy_context()