import subprocess
import time
import tempfile
from pathlib import Path


class YdoToold:
    def __init__(self):
        self._socket = Path(tempfile.gettempdir()).joinpath(
            "pydotool-{}.socket".format(id(self))
        )
        self._process = subprocess.Popen(
            ["ydotoold", "--socket-path", self._socket],
            stdout=None,
            stdin=None,
            stderr=None,
            close_fds=True,
            start_new_session=True,
        )
        # default sleep added for udev to kick in
        time.sleep(0.500)

    def __del__(self):
        self._process.terminate()
        self._process.wait()

    @property
    def socket(self):
        return str(self._socket)
