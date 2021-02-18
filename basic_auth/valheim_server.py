import os
import subprocess
import time

from flask import Flask

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
            if time_since_reset < self.flask.config['RESET_TIMER']:
                return self.curr_state

        stat = os.system('systemctl is-active --quiet valheimserver')
        self.curr_state = _STATE['on'] if stat == 0 else _STATE['off']

        return self.curr_state

    def reset_server(self):
        if self.curr_state == _STATE['reset']:
            return self.curr_state

        try:
            subprocess.Popen(self.flask.config['RESET_CMD'])
        except Exception:
            print("Reset command invalid: %s" % self.flask.config['RESET_CMD'])

        self.curr_state = _STATE['reset']
        self.reset_start_time = time.perf_counter()

        return self.curr_state
