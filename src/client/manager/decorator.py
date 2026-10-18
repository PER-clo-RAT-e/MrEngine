class DecoratorManager:
    def __init__(self) -> None:
        self._decorators = {}

    def set(self, path: str, decorator):
        node = self._decorators
        parts = path.split('.')

        for part in parts[:-1]:
            node = node.setdefault(part, {})

        node[parts[-1]] = decorator


    def deco(self, path: str):
        node = self._decorators
        parts = path.split('.')

        for part in parts:
            if part not in node:
                return self._dummy
            node = node[part]

        if not callable(node):
            node = self._dummy

        return node


    def _dummy(self, path: str):
        def _dummy_deco(func):
            def dummy_wrapper(*args, **kwargs):
                print(f"DECORATOR NIT SPECIFIED FOR {path}")

                result = func(args, kwargs)

                print(f"DECORATOR NIT SPECIFIED FOR {path}")

                return result
            return dummy_wrapper
        return _dummy_deco

    def __call__(self, path: str):
        return self.deco(path)
