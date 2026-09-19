from cmath import exp
from enum import auto, StrEnum
import time
import pygame
import os
import readchar

from threading import Thread
from client.manager.mod.manager import BaseManager
from client.manager.mod.state import Status
from client.manager.event import ApplicationEvent, EventManager

class InputEvent(StrEnum):
    KEY_PRESSED     = auto()
    KEY_RELEASED    = auto()
    JOY_CONNECTED   = auto()
    JOY_REMOVED     = auto()


class InputManager(BaseManager):
    def __init__(self, event_manager: EventManager) -> None:
        super().__init__()

        self._event_manager = event_manager

        self._event_manager.subscribe(ApplicationEvent.TERMINATE,
            lambda: self._state.set_status(Status.SHUTDOWN))

        os.environ["SDL_VIDEODRIVER"] = "dummy"

        pygame.init()
        pygame.display.set_mode((1,1))

        pygame.joystick.init()

        self.joystics = {}

        self._state.set_status(Status.IDLE)

    def demonise(self) -> tuple[Thread, Thread]:
        thread_gp = Thread(target=self._cycle_gp, daemon=True)
        thread_gp.start()
        thread_kb = Thread(target=self._cycle_kb, daemon=True)
        thread_kb.start()

        return thread_kb, thread_gp

    def _cycle_gp(self):
        ev = self._event_manager

        try:

            while self.status not in [Status.ATERROR, Status.SHUTDOWN]:
                for event in pygame.event.get():
                    match event.type:
                        case pygame.JOYDEVICEADDED:
                            pad = pygame.joystick.Joystick(event.device_index)
                            self.joystics[pad.get_instance_id()] = pad

                            ev.emit(InputEvent.JOY_CONNECTED, pad.get_name())

                        case pygame.JOYDEVICEREMOVED:
                            pad = self.joystics[event.instance_id]
                            ev.emit(InputEvent.JOY_REMOVED, pad.get_name())

                            del pad



                time.sleep(0.01)
        except KeyboardInterrupt:
            ev.emit(ApplicationEvent.TERMINATE)

    def _cycle_kb(self):
        ev = self._event_manager
        while self.status != Status.ATERROR:
            key = readchar.readkey()
            if key:
                ev.emit(InputEvent.KEY_PRESSED, key)
