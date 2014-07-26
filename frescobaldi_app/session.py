# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2014 by Wilbert Berendsen
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
Stuff dealing with the QSessionManager.
"""

from __future__ import unicode_literals

import os
import sys

from PyQt4.QtCore import QObject, QSettings, Qt, SIGNAL
from PyQt4.QtGui import QApplication, QSessionManager

import info
import app
import mainwindow


def sessionSettings(key):
    """Returns the QSettings object for sessiondata of the specified key."""
    settings = QSettings()
    settings.beginGroup("sessiondata")
    settings.beginGroup(key)
    return settings


def commitData(sm):
    """Save a session on behalf of the session manager."""
    if not sm.allowsInteraction():
        pass # TODO: can implement saving unsaved/unnamed docs to cache buffers
    sm.release()
    key = sm.sessionKey()
    saveSession(key)


def saveSession(key):
    """Save the current session under key."""
    settings = sessionSettings(key)
    settings.setValue('numwindows', len(app.windows))
    for index, win in enumerate(app.windows):
        settings.beginGroup("mainwindow{0}".format(index))
        win.writeSessionSettings(settings)
        settings.endGroup()
    settings.sync()


def restoreSession(key):
    """Restore a session specified by key, previously saved by the session manager."""
    settings = sessionSettings(key)
    for index in range(settings.value('numwindows', 0, int)):
        settings.beginGroup("mainwindow{0}".format(index))
        win = mainwindow.MainWindow()
        win.readSessionSettings(settings)
        win.show()
        settings.endGroup()


@app.oninit
def _setup():
    # the new-style way of connecting fails on PyQt4 4.8.x...
    QObject.connect(app.qApp, SIGNAL("commitDataRequest(QSessionManager&)"), commitData)


