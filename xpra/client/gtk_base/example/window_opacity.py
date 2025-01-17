#!/usr/bin/env python3
# Copyright (C) 2020 Antoine Martin <antoine@xpra.org>
# Xpra is released under the terms of the GNU GPL v2, or, at your option, any
# later version. See the file COPYING for details.

from xpra.platform import program_context
from xpra.platform.gui import force_focus
from xpra.gtk_common.gtk_util import add_close_accel, get_icon_pixbuf

import gi
gi.require_version("Gtk", "3.0")  # @UndefinedVariable
from gi.repository import Gtk, GLib   #pylint: disable=wrong-import-position @UnresolvedImport

opacity = 50

def make_window():
    win = Gtk.Window()
    win.set_position(Gtk.WindowPosition.CENTER)
    win.set_title('Opacity Test')
    win.connect('delete-event', Gtk.main_quit)
    icon = get_icon_pixbuf("windows.png")
    if icon:
        win.set_icon(icon)

    btn = Gtk.Button(label="Change Opacity")
    def change_opacity(*_args):
        global opacity
        opacity = (opacity + 5) % 100
        btn.set_label("Change Opacity: %i%%" % opacity)
        win.set_opacity(opacity/100.0)
    btn.connect('clicked', change_opacity)
    win.add(btn)
    change_opacity()
    return win

def main():
    with program_context("window-opacity", "Window Opacity"):
        w = make_window()
        def show_with_focus():
            force_focus()
            w.show_all()
            w.present()
        add_close_accel(w, Gtk.main_quit)
        from xpra.gtk_common.gobject_compat import register_os_signals
        def signal_handler(*_args):
            Gtk.main_quit()
        register_os_signals(signal_handler)
        GLib.idle_add(show_with_focus)
        Gtk.main()
        return 0


if __name__ == '__main__':
    main()
