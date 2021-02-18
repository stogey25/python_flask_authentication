import os
import subprocess
import time

from flask import Flask

_RESET_TIMEOUT_SEC = 120
_STATE = {"on": "Online", "off": "Offline", "reset": "Resetting"}


class ValheimServer(object):
    """Single instance of a Valheim Server."""

    def __init__(self, name):
        self.flask = Flask(name)
        self.curr_state = _STATE['off']
        self.reset_start_time = None

    def get_server_status(self):
        if self.curr_state == _STATE['reset']:
            time_since_reset = time.perf_counter() - self.reset_start_time
            if time_since_reset < _RESET_TIMEOUT_SEC:
                return self.curr_state

        stat = os.system('systemctl is-active --quiet valheimserver')
        self.curr_state = _STATE['on'] if stat == 0 else _STATE['off']

        return self.curr_state

    def reset_server(self):
        if self.curr_state == _STATE['reset']:
            return self.curr_state

        subprocess.Popen(['ls', '-l'])
    #    subprocess.Popen('/usr/local/bin/valheimbackup')
        self.curr_state = _STATE['reset']
        self.reset_start_time = time.perf_counter()

        return self.curr_state
