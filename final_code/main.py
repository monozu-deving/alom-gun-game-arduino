import random
import serial
import time
from dearpygui import dearpygui as dpg
numlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
current_target = random.choice(numlist)
button_ser = serial.Serial('COM6', 9600, timeout=0.1)
relay_ser = serial.Serial('COM8', 9600, timeout=0.1)
time.sleep(2)

CELL_WIDTH = 150
CELL_HEIGHT = 150
GRID_COLS = 3
GRID_ROWS = 4
score = 0
message = "click button and start!"


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
def set_target(target):
    # 10,11,12은 'a','b','c'
    cmd = str(target) if target < 10 else chr(ord('a') + target - 10)
    # time.sleep(1)
    relay_ser.write(cmd.encode())
    dpg.set_value("target_text", f"Object: {target}")

def check_hit():
    global score, current_target, message
    try:
        line = button_ser.readline().decode(errors='ignore').strip()
        if line.isdigit():
            val = int(line)
            if val == current_target:
                score += 1
                message = f"Answer button {val}"
                dpg.set_value("score_text", f"Score: {score}")
                current_target = random.choice(numlist)
                set_target(current_target)
                draw_grid()
            else:
                message = f"Wrong: {val} (hope: {current_target})"
        dpg.set_value("message_text", message)
    except:
        pass

dpg.create_context()
with dpg.window(label="UFO Grid Game", tag="main"):
    dpg.add_text(f"Object: {current_target}", tag="target_text")
    dpg.add_text(f"score: 0", tag="score_text")
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
