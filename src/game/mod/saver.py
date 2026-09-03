from pathlib import PosixPath

class Saver:
    def __init__(self, path=PosixPath):
        self.save_path = path

    def save_preferences(self, mines, dimensions) -> str:
        if dimensions == None or mines == None:
            return "empty_pref"
