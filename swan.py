#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

"""
This script uses the i3ipc python library to create dynamic workspace names in
Sway.

Author: Fabio Noris
e-mail: info@norisfabio.com
Project: https://github.com/fnoris/swan
License: GPL3

Dependencies: python-i3ipc>=2.0.1 (i3ipc-python)
"""

from i3ipc import Connection
import signal
import sys


# Icons for common programs. Add or edit your custom variables here.
# Keys are app_id variables (Wayland app) or class (XWayland)
# from the output of 'swaymsg -t get_tree | grep "app_id\|class"',
# values are character codes or text you want to display.
# (font awesome: http://fortawesome.github.io/Font-Awesome/icons/
FA_BOOK = '\uf02d'
FA_CHROME = '\uf268'
FA_CODE = '\uf121'
FA_FILE_PDF_O = '\uf1c1'
FA_FILE_TEXT_O = '\uf15c'
FA_FILE_WORD_O = '\uf1c2'
FA_FILE_EXCEL_O = '\uf1c3'
FA_FILE_POWERPOINT_O = '\uf1c4'
FA_FOLDER = '\uf07b'
FA_FONT = '\uf031'
FA_FIREFOX = '\uf269'
FA_LOCK = '\uf023'
FA_USER_SECRET = '\uf21b'
FA_MUSIC = '\uf001'
FA_PAINT_BRUSH = '\uf1fc'
FA_PENCIL = '\uf303'
FA_PICTURE_O = '\uf03e'
FA_VNC = '\uf26c'
FA_TERMINAL = '\uf120'
FA_DOWNLOAD = '\uf019'
FA_DESKTOP = '\uf108'
FA_EYE = '\uf06e'
FA_REBEL = '\uf1d0'
FA_KEY = '\uf084'
FA_TASKS = '\uf0ae'
FA_COGS = '\uf085'
FA_PRODUCT_HUNT = '\uf288'
FA_SEARCH = '\uf002'
FA_YOUTUBE_PLAY = '\uf16a'
FA_COMMENT_O = '\uf0e5'
FA_WINDOWS = '\uf17a'
FA_LINUX = '\uf1d6'
FA_BTC = '\uf15a'
FA_GLOBE = '\uf0ac'
FA_FLOPPY = '\uf0c7'
FA_SKYPE = '\uf17e'

# Default icon/text for unknown apps
DEFAULT_ICON = '\uf059'
EMPTY_WS = ''

APP_ICONS = {
    'urxvt256c': FA_TERMINAL,
    'urxvt256cc': FA_TERMINAL,
    'gnome-terminal-server': FA_TERMINAL,
    'kitty': FA_TERMINAL,
    'alacritty': FA_TERMINAL,
    'xterm': FA_TERMINAL,
    'st-256color': FA_TERMINAL,
    'google-chrome': FA_CHROME,
    'chromium-browser': FA_CHROME,
    'chromium-freeworld': FA_CHROME,
    'subl': FA_CODE,
    'subl3': FA_CODE,
    'firefox': FA_FIREFOX,
    'firefox developer edition': FA_FIREFOX,
    'tor browser': FA_REBEL,
    'libreoffice-startcenter': FA_FILE_TEXT_O,
    'libreoffice': FA_FILE_TEXT_O,
    'libreoffice-writer': FA_FILE_WORD_O,
    'libreoffice-calc': FA_FILE_EXCEL_O,
    'libreoffice-impress': FA_FILE_POWERPOINT_O,
    'jetbrains-idea-ce': FA_CODE,
    'code': FA_CODE,
    'feh': FA_PICTURE_O,
    'sxiv': FA_PICTURE_O,
    'nitrogen': FA_PICTURE_O,
    'mupdf': FA_FILE_PDF_O,
    'evince': FA_FILE_PDF_O,
    'org.gnome.nautilus': FA_FOLDER,
    'transmission-gtk': FA_DOWNLOAD,
    'vlc': FA_YOUTUBE_PLAY,
    'mpv': FA_YOUTUBE_PLAY,
    'calibre-gui': FA_BOOK,
    'calibre': FA_BOOK,
    'org.remmina.remmina': FA_DESKTOP,
    'x2goclient': FA_DESKTOP,
    'x2goagent': FA_DESKTOP,
    'skype': FA_SKYPE,
    'nxagent': FA_DESKTOP,
    'pyhoca-gui': FA_DESKTOP,
    'wireshark': FA_EYE,
    'seahorse': FA_KEY,
    'gimp-2.8': FA_PAINT_BRUSH,
    'gimp-2.10': FA_PAINT_BRUSH,
    'virt-manager': FA_TASKS,
    'virt-viewer': FA_WINDOWS,
    'gnome-boxes': FA_WINDOWS,
    'gnome-font-viewer': FA_FONT,
    'nm-connection-editor': FA_COGS,
    'crx_bikioccmkafdpakkkcpdbppfkghcmihk': FA_COMMENT_O,
    'electrum': FA_BTC,
    'qutebrowser': FA_GLOBE,
    'teamviewer': FA_DESKTOP,
    'uzbl-core': FA_GLOBE,
    'com-sonicwall-netextender': FA_LOCK,
    'packettracer7': FA_PRODUCT_HUNT,
    'filezilla': FA_FLOPPY,
    'com-install4j-runtime-launcher-UnixLauncher': FA_USER_SECRET,
    'krita': FA_PENCIL,
}


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
                        win_name += APP_ICONS.get(str.lower(w.app_id), DEFAULT_ICON) + ' '
                    # xwayland app
                    elif w.window_class:
                        win_name += APP_ICONS.get(str.lower(w.window_class), DEFAULT_ICON) + ' '
                ws_new_name = "%s: %s" % (workspace.num, win_name)
                wm.command('rename workspace "%s" to %s' % (ws_old_name, ws_new_name))
            # No open window(s), name empty workspace
            else:
                ws_new_name = "%s: %s" % (workspace.num, EMPTY_WS)
                wm.command('rename workspace "%s" to %s' % (ws_old_name, ws_new_name))
    except Exception as ex:
        # print("Exception: ", ex)
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
    ## this causes problem on i3 - test on sway
    #wm.on('workspace', window_event_handler)
    wm.main()


if __name__ == "__main__":
    main()
