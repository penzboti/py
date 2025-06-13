https://python-mss.readthedocs.io/examples.html#playing-with-pixels
https://pyautogui.readthedocs.io/en/latest/mouse.html

from mss import mss
import keyboard
import pyautogui

run = False

def change_run():
    global run
    run = not run

# toggle on or off (or just close?)
keyboard.on_press_key("p", lambda _:change_run())

def handle_screenshot(mss):
    mss.shot()

    # get mouse pos
    currentMouseX, currentMouseY = pyautogui.position()
    # set mouse pos and click
    pyautogui.click(100, 200)

    # shotgun
    pyautogui.mouseDown(button='right',x=100,y=200); pyautogui.mouseUp()
    # and then just click


def main():
    # print("hello")
    with mss() as sct:
        while True:
            pass
    #     handle_screenshot(sct)

main()
