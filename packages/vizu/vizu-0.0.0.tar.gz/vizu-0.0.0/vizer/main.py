import sys
import pandas as pd

import socket
from contextlib import closing
import webbrowser

import logging
from vizer.gui import create_webapp

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def run():

    df = pd.read_csv(sys.argv[1])

    app = create_webapp(df)

    p = find_free_port()
    webbrowser.open(f"http://localhost:{p}")
    app.run_server(port=p, host="0.0.0.0", debug=False)


if __name__ == "__main__":
    run()
