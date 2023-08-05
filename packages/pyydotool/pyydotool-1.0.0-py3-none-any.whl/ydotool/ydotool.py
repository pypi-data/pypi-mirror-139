import subprocess
import time
from typing import Optional
from ydotool.daemon import YdoToold

_command = "ydotool"


class YdoTool:
    def __init__(self, daemon: Optional[YdoToold] = None):
        self.instructions = []
        self._daemon = daemon
        if daemon is None:
            self._daemon = YdoToold()

    def exec(self):
        """
        execute command queue
        """
        for instruction in self.instructions:
            instruction()
        return self

    def reset(self):
        """
        clean command queue
        """
        self.instructions = []
        return self

    def _add_instruction(self, instruction: callable):
        self.instructions.append(instruction)

    @staticmethod
    def command(fun: callable):
        def command_wrapper(self, *args, **kwargs):
            out = fun(self, *args, **kwargs)

            def wrapper():
                command = subprocess.run(
                    [_command] + out,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env={"YDOTOOL_SOCKET": self._daemon.socket},
                )
                if command.returncode != 0:
                    raise Exception(command.stderr)

            self._add_instruction(wrapper)
            return self

        return command_wrapper

    @staticmethod
    def py_command(fun: callable):
        def py_wrapper(self, *args, **kwargs):
            out = fun(self, *args, **kwargs)
            fn = out.pop(0)

            def wrapper():
                return fn(*out)

            self._add_instruction(wrapper)
            return self

        return py_wrapper

    @staticmethod
    def _parse_options(**kwargs):
        opts = []
        for key, value in kwargs.items():
            if value is True:
                opts.append(f"--{key}")
            elif value is not False or value is not None:
                opts.extend([f"--{key}", value])
        return opts

    @py_command
    def sleep(self, delay: float):
        return [time.sleep, delay]

    @command
    def key(self, *keys, **kwargs):
        if isinstance(keys[0], list):
            keys = keys[0]
        if not all(lambda x: isinstance(x, str)):
            raise TypeError("Not all keys in sequence are strings")
        opts = self._parse_options(**kwargs)
        return ["key"] + opts + keys

    @command
    def type(self, texts: str, **kwargs):
        opts = self._parse_options(**kwargs)
        return ["type", texts] + opts

    @command
    def mousemove(self, x: int, y: int, **kwargs):
        opts = self._parse_options(**kwargs)
        return ["mousemove"] + opts + ["--", str(x), str(y)]

    @command
    def click(self, buttons: str, **kwargs):
        opts = self._parse_options(**kwargs)
        return ["click", buttons] + opts
