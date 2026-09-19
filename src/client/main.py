import time
from blessed import Terminal
import numpy as np

from client.manager.event import EventManager
from client.manager.graphic import GraphicManager
from client.manager.input import InputEvent, InputManager
from client.manager.mod.objects.ui.button import BaseButton


def main():

    event_manager = EventManager()
    input_manager = InputManager(event_manager)
    graphic_manager = GraphicManager(event_manager)

    thread1, thread2 = input_manager.demonise()
    thread3 = graphic_manager.demonise()

    btn = BaseButton((20, 20), (32, 16), (1, 2, 1, 2), " Button")
    btn1 = BaseButton((60, 50), (32, 16), (1, 2, 1, 2), " Button")
    btn2 = BaseButton((110, 70), (32, 16), (1, 2, 1, 2), " Button")
    btn3 = BaseButton((160, 80), (32, 16), (1, 2, 1, 2), " Button")

    graphic_manager.add_bg_elemnt('btn', btn)
    graphic_manager.add_bg_elemnt('btn1', btn1)
    graphic_manager.add_bg_elemnt('btn2', btn2)
    graphic_manager.add_bg_elemnt('btn3', btn3)

    event_manager.subscribe(InputEvent.JOY_CONNECTED, react_to_connection)
    event_manager.subscribe(InputEvent.JOY_REMOVED, react_to_disconnection)

    event_manager.subscribe(InputEvent.KEY_PRESSED, react_to_press)
    event_manager.subscribe(InputEvent.KEY_RELEASED, react_to_release)

    time.sleep(10)


def react_to_connection(dev_name):
    print(f"Joy Device connected: {dev_name}")

def react_to_disconnection(dev_name):
    print(f"Joy Device disconnected: {dev_name}")


def react_to_press(key_name):
        print(f"Pressed key: {key_name}")

def react_to_release(key_name):
        print(f"Released key {key_name}")


if __name__ == "__main__":
    main()
