import random
import serial
import time
from dearpygui import dearpygui as dpg

# # 시리얼 포트 설정 (환경에 맞게 수정)
# ser = serial.Serial('COM4', 9600, timeout=1)
# time.sleep(2)

CELL_WIDTH = 250
CELL_HEIGHT = 200
GRID_COLS = 3
GRID_ROWS = 4
current_target = 1
slave_addresses = [8, 9, 10]
waiting = False

def send_target_to_arduino(target_number):
    slave = (target_number - 1) // 4 + 8
    index = (target_number - 1) % 4
    cmd = f"SET {slave} {index}\n"
    # ser.write(cmd.encode())
    print(f"📤 Sent to Arduino: {cmd.strip()}")

# def check_hit():
#     for addr in slave_addresses:
        # ser.write(f"GET {addr}\n".encode())
        # line = ser.readline().decode().strip()
        # # if line.startswith("RESULT"):
        #     _, a, v = line.split()
        #     if int(v) == 1:
        #         return int(a)
    # return None

def draw_grid():
    dpg.delete_item("ufo_canvas", children_only=True)
    for i in range(12):
        row = i // GRID_COLS
        col = i % GRID_COLS
        x = col * CELL_WIDTH
        y = row * CELL_HEIGHT
        dpg.draw_rectangle((x, y), (x + CELL_WIDTH, y + CELL_HEIGHT), color=(50, 50, 50, 255), parent="ufo_canvas")
        dpg.draw_text((x + 10, y + 10), text=str(i + 1), size=20, color=(255, 255, 255, 255), parent="ufo_canvas")

def set_new_target():
    global current_target, waiting
    draw_grid()
    current_target = random.randint(1, 12)
    row = (current_target - 1) // GRID_COLS
    col = (current_target - 1) % GRID_COLS
    x = col * CELL_WIDTH + CELL_WIDTH // 2
    y = row * CELL_HEIGHT + CELL_HEIGHT // 2
    dpg.draw_circle((x, y), 40, color=(150, 150, 150, 255), fill=(100, 255, 100, 255), parent="ufo_canvas")
    dpg.set_value("target_label", f"🎯 Current Target: {current_target}")
    send_target_to_arduino(current_target)
    waiting = True

# def check_hit_and_loop():
#     global waiting
#     if waiting:
#         hit = check_hit()
#         if hit is not None:
#             if hit == (current_target - 1) // 4 + 8:
#                 print(f"✅ Correct hit from slave {hit}!")
#                 set_new_target()

dpg.create_context()

with dpg.window(label="UFO Grid Game", tag="main_window"):
    with dpg.drawlist(width=GRID_COLS * CELL_WIDTH, height=GRID_ROWS * CELL_HEIGHT, tag="ufo_canvas"):
        pass
    dpg.add_text("🎯 Current Target: 1", tag="target_label")

set_new_target()

with dpg.handler_registry():
    dpg.add_mouse_click_handler(callback=lambda: None)  # 필수: 이벤트 루프 유지용

dpg.create_viewport(title="UFO Grid Game", width=1200, height=700)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("main_window", True)

# 메인 루프에서 반복 검사
while dpg.is_dearpygui_running():
    # check_hit_and_loop()
    dpg.render_dearpygui_frame()
    time.sleep(0.1)

dpg.destroy_context()