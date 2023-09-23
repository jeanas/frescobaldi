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
The help browser window.
"""


from pathlib import Path

from PyQt5.QtCore import QSettings, QSize, Qt, QUrl
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtPrintSupport import QAbstractPrintDialog, QPrintDialog, QPrinter

import app
import i18n.setup
import icons

class Window(QMainWindow):
    """The help browser window."""
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_QuitOnClose, False)

        self.webview = QWebEngineView(self)
        self.setCentralWidget(self.webview)

        self._toolbar = tb = self.addToolBar('')
        self._back = tb.addAction(icons.get('go-previous'), '')
        self._forw = tb.addAction(icons.get('go-next'), '')
        self._home = tb.addAction(icons.get('go-home'), '')
        self._print = tb.addAction(icons.get('document-print'), '')
        self._back.triggered.connect(self.webview.back)
        self._forw.triggered.connect(self.webview.forward)
        self._home.triggered.connect(self.home)
        self._print.triggered.connect(self.print_)

        app.translateUI(self)
        self.loadSettings()

    def closeEvent(self, ev):
        self.saveSettings()
        super().closeEvent(ev)

    def loadSettings(self):
        self.resize(QSettings().value("helpbrowser/size", QSize(400, 300), QSize))

    def saveSettings(self):
        QSettings().setValue("helpbrowser/size", self.size())

    def translateUI(self):
        # self.setCaption() # TODO
        self._toolbar.setWindowTitle(_("Toolbar"))
        self._back.setText(_("Back"))
        self._forw.setText(_("Forward"))
        self._home.setText(_("Start"))
        self._print.setText(_("Print"))
        self.setWindowTitle(_("Help"))

    def home(self):
        self.displayPage('index')

    def displayPage(self, name=None):
        """Opens the help browser showing the specified help page."""
        if name is None:
            name = "index"

        def get_path(lang):
            return (Path(__file__).parent / "build" / lang / name).with_suffix(".html")

        path = get_path(i18n.setup.current().split("_")[0])
        if not path.exists(): # certain languages don't have user guide translations
            path = get_path("en")

        self.webview.load(QUrl.fromLocalFile(str(path)))
        self.show()
        self.activateWindow()
        self.raise_()

    def print_(self):
        printer = self._printer = QPrinter()
        dlg = QPrintDialog(printer, self)
        dlg.setWindowTitle(app.caption(_("Print")))
        if dlg.exec_():
            self.webview.page().print(printer, self.slotPrintingDone)

    def slotPrintingDone(self, success):
        del self._printer
