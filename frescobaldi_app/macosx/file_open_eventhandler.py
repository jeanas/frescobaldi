# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2013 - 2014 by Wilbert Berendsen
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# See http://www.gnu.org/licenses/ for more information.

"""
This handles the QEvent::FileOpen event type sent to the QApplication when
a file is clicked in the file manager.

Currently this makes only sense on Mac OS X.
"""


from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtWidgets import QApplication

import app


handler = None
_initial_files_opened = []

def openUrl(url):
    """Open Url.

    If there is an active MainWindow, the document is made the current
    document in that window. If there is no MainWindow at all, it is
    created.

    """
    win = app.activeWindow()
    if not win:
        import mainwindow
        win = mainwindow.MainWindow()
        win.show()
    d = win.openUrl(url)
    if d:
        win.setCurrentDocument(d)


# This is a little tricky: when we receive a FileOpen event, there
# are two cases. Either the user opened a file in the Finder while
# Frescobaldi was not open, in which case Frescobaldi gets fired up.
# Or Frescobaldi was already open, in which case the file is just
# opened in a new tab of the existing window. In the former case,
# we must not create a new window, instead we must add the document
# to the list of initial documents for the main window that is to be
# created soon.

class FileOpenEventHandler(QObject):
    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.FileOpen:
            openUrl(ev.url())
            return True
        return False

class InitializationFileOpenEventHandler(QObject):
    def eventFilter(self, obj, ev):
        if ev.type() == QEvent.FileOpen:
            _initial_files_opened.append(ev.url())
            return True
        return False

def initialize():
    global handler
    # First get the initial events
    handler = InitializationFileOpenEventHandler()
    app.qApp.installEventFilter(handler)
    app.qApp.processEvents()
    app.qApp.removeEventFilter(handler)
    # Then leave a handler for other events
    handler = FileOpenEventHandler()
    app.qApp.installEventFilter(handler)


def initial_files_opened():
    """Return the list of files that were triggered the launch of Frescobaldi
    by being opened in the Finder."""
    return _initial_files_opened
