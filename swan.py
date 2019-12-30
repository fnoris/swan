#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This script uses the i3ipc python library to create dynamic workspace names
in i3/sway.

Author: Fabio Noris
e-mail: info@norisfabio.com
Project: https://github.com/fnoris/swan
License: GPL3
Version: 1.0

Dependencies: python-i3ipc>=2.0.1 (i3ipc-python)
"""

from i3ipc import Connection
from configparser import ConfigParser, ExtendedInterpolation
import signal
import sys
import os


CONFIG_PATH = os.environ['HOME'] + '/.config/swan/'
CONFIG_NAME = 'swan.conf'
CONFIG_FILE = CONFIG_PATH + CONFIG_NAME

# read config file if exists or create a default one
conf = ConfigParser(interpolation=ExtendedInterpolation())

if not os.path.exists(CONFIG_FILE):
    conf['DEFAULT'] = {'DEFAULT_ICON': '', 'EMPTY_WS': '', 'DEBUG': 'false'}
    conf['icons'] = {'APP_ICON': ''}
    conf['applications'] = {'APP_NAME': '${icons:APP_ICON}'}
    os.makedirs(CONFIG_PATH, exist_ok=True)
    conf.write(open(CONFIG_FILE, 'w'))
else:
    conf.read(CONFIG_FILE)

app_icons = conf['applications']
default_icon = conf.get('DEFAULT', 'DEFAULT_ICON', fallback='\uf059')
empty_ws = conf.get('DEFAULT', 'EMPTY_WS', fallback='')
debug = conf.get('DEFAULT', 'DEBUG', fallback='false')

# Create Connection object used to send commands and subscribe to events
wm = Connection()


def change_ws_names(wm, e):
    # This function (re)names workspaces after open window(s), if any
    try:
        for ws_index, workspace in enumerate(wm.get_tree().workspaces()):
            ws_old_name = workspace.name
            win_name = ''
            # Check for open window(s) in ws_index workspace
            if workspace.leaves():
                for w in workspace.leaves():
                    # wayland native app
                    if w.app_id:
                        win_name += app_icons.get(str.lower(w.app_id), default_icon) + ' '
                    # xwayland app
                    elif w.window_class:
                        win_name += app_icons.get(str.lower(w.window_class), default_icon) + ' '
                ws_new_name = "%s: %s" % (workspace.num, win_name)
                wm.command('rename workspace "%s" to %s' % (ws_old_name, ws_new_name))
            # No open window(s), name empty workspace
            else:
                ws_new_name = "%s: %s" % (workspace.num, empty_ws)
                wm.command('rename workspace "%s" to %s' % (ws_old_name, ws_new_name))
    except Exception as ex:
        if debug == 'true':
            print("Exception: ", ex)
        exit(ex)


def signal_handler(signal, frame):
    # Exit gracefully when swan is terminated
    for workspace in wm.get_tree().workspaces():
        # rename workspaces to just numbers on exit
        wm.command('rename workspace "%s" to "%d"' % (workspace.name, workspace.num))
    wm.main_quit()
    sys.exit(0)


def main():
    # Exit gracefully when terminated
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Call change_ws_names() for subscribed window and workspace events
    def window_event_handler(wm, e):
        if e.change in ['new', 'close', 'move']:
            change_ws_names(wm, e)

    wm.on('window', window_event_handler)
    # this causes problem on i3 - test on sway
    # wm.on('workspace', window_event_handler)
    wm.main()


if __name__ == "__main__":
    main()
