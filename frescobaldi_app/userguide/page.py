# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2013 - 2013 by Wilbert Berendsen
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
Page, a page from the Frescobaldi User Manual.
"""

from __future__ import unicode_literals

import re

from PyQt4.QtCore import QKeySequence

import simplemarkdown

from . import read
from . import resolve


class Page(object):
    def __init__(self, name=None):
        self._attrs = {}
        self._title = "No Title"
        self._body = ""
        if name:
            self.load(name)
    
    def load(self, name):
        doc, attrs = read.document(name)
        self.parse_text(doc, attrs)
        
    def parse_text(self, text, attrs=None):
        self._attrs = attrs or {}
        t = simplemarkdown.Tree()
        # parse and translate the document
        read.Parser().parse(text, t)
        # title
        for heading in t.find('heading'):
            self._title = t.text(heading)
            break
        html = t.html()
        # resolve variables...
        html = Resolver(attrs.get('VARS')).format(html)
        # remove empty paragraphs (could result from optional text)
        html = html.replace('<p></p>', '')
        self._body = html
    
    def is_popup(self):
        """Return True if the helppage should be displayed as a popup."""
        try:
            return 'popup' in self._attrs['PROPERTIES']
        except KeyError:
            return False
    
    def title(self):
        """Return the title"""
        return self._title
    
    def body(self):
        """Return the HTML body."""
        return self._body
        
    def children(self):
        """Return the list of names of child documents."""
        return self._attrs.get("SUBDOCS") or []
    
    def seealso(self):
        """Return the list of names of "see also" documents."""
        return self._attrs.get("SEEALSO") or []


class Resolver(object):
    """Resolves variables in help documents."""
    
    _rx = re.compile(r"\{([a-z]+(_[a-z]+)*)\}", re.UNICODE)
    def __init__(self, variables=None):
        """Initialize with a list of variables from the #VARS section.
        
        Every item is simply a line, where the first word is the name,
        the second the type and the rest is the contents.
        
        """
        self._variables = d = {}
        if variables:
            for v in variables:
                name, type, text = v.split(None, 2)
                d[name] = (type, text)
    
    def format(self, text):
        """Replaces all {variable} items in the text."""
        return self._rx.sub(self.replace, text)
        
    def replace(self, matchObj):
        result = self.resolve(matchObj.group(1))
        return result if result else matchObj.group()
    
    def resolve(self, name):
        try:
            typ, text = self._variables[name]
        except KeyError:
            try:
                return getattr(resolve, name)()
            except AttributeError:
                return
        try:
            method = getattr(self, 'handle_' + typ.lower())
        except AttributeError:
            method = self.handle_text
        return method(text)

    def handle_md(self, text):
        """Convert inline markdown to HTML."""
        return simplemarkdown.html_inline(text)

    def handle_html(self, text):
        """Return text as is, it may contain HTML."""
        return text
    
    def handle_text(self, text):
        """Return text escaped, it will not be represented as HTML."""
        return simplemarkdown.html_escape(text)

    def handle_url(self, text):
        """Return a clickable url."""
        url = text
        if text.startswith('http://'):
            text = text[7:]
        if text.endswith('/'):
            text = text[:-1]
        url = simplemarkdown.html_escape(url).replace('"', '&quot;')
        text = simplemarkdown.html_escape(text)
        return '<a href="{0}">{1}</a>'.format(url, text)

    def handle_help(self, text):
        """Return a link to the specified help page, with the title."""
        try:
            title = Page(text).title()
        except (OSError, IOError):
            title = text
        url = text
        return '<a href="{0}">{1}</a>'.format(url, title)

    def handle_shortcut(self, text):
        """Return the keystroke currently defined for the action."""
        collection_name, action_name = text.split(None, 1)
        import actioncollectionmanager
        mgr = actioncollectionmanager.ActionCollectionManager.instances()[0]
        seq = mgr.action(collection_name, action_name).shortcut()
        key = seq.toString(QKeySequence.NativeText) or _("(no key defined)")
        return '<span class="shortcut">{0}</span>'.format(simplemarkdown.html_escape(key))

