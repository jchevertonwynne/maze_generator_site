#!/usr/local/bin/python3

import sys

from secret import secret
from maze_site_app import setup_app


def main():
    reset_database = "-r" in sys.argv
    app = setup_app(secret=secret, reset=reset_database)

    if "-i" in sys.argv:
        app.run(host="0.0.0.0", port=80)
    else:
        app.run()


if __name__ == "__main__":
    main()
