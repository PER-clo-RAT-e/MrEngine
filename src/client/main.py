import time
from blessed import Terminal
import numpy as np

from client.manager.event import ApplicationEvent, EventManager
from client.manager.graphic import GraphicManager
from client.manager.input import InputEvent, InputManager
from client.manager.mod.objects.ui.button import BaseButton2D
from client.manager.mod.objects.ui.line import BaseLine2D


def main():
    event_manager = EventManager()
    input_manager = InputManager(event_manager)
    graphic_manager = GraphicManager(event_manager)

    thread1, thread2 = input_manager.demonise()
    thread3 = graphic_manager.demonise()

    btn = BaseButton2D("0", (20, 20), (32, 16), (1, 2, 1, 2), "Button text")
    btn1 = BaseButton2D("1", (60, 50), (32, 16), (1, 2, 1, 2), "Button lalala ")
    btn2 = BaseButton2D("2", (110, 70), (32, 16), (1, 2, 1, 2), "Button lalala")
    btn3 = BaseButton2D("3", (160, 80), (32, 16), (1, 2, 1, 2), "Buttonlalall lal allalala")

    ln1 = BaseLine2D("4", (10, 6), (80, 1), 0)

    graphic_manager.add_bg_elemnt('btn', btn)
    graphic_manager.add_bg_elemnt('btn1', btn1)
    graphic_manager.add_bg_elemnt('btn2', btn2)
    graphic_manager.add_bg_elemnt('btn3', btn3)

    event_manager.subscribe(InputEvent.JOY_CONNECTED, react_to_connection)
    event_manager.subscribe(InputEvent.JOY_REMOVED, react_to_disconnection)

    event_manager.subscribe(InputEvent.KEY_PRESSED, react_to_press)
    event_manager.subscribe(InputEvent.KEY_RELEASED, react_to_release)

    try:
        while 1:
            time.sleep(0.1)

    except KeyboardInterrupt:
        event_manager.emit(ApplicationEvent.TERMINATE)


def react_to_connection(dev_name):
    print(f"Joy Device connected: {dev_name}")

def react_to_disconnection(dev_name):
    print(f"Joy Device disconnected: {dev_name}")


def react_to_press(key_name):
        print(f"Pressed key: {key_name}")

def react_to_release(key_name):
        print(f"Released key {key_name}")
