# This file is part of the Frescobaldi project, http://www.frescobaldi.org/
#
# Copyright (c) 2008 - 2011 by Wilbert Berendsen
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
Use this module to get the parsed tokens of a document.

The tokens are created by the syntax highlighter, see highlighter.py.
The core methods of this module are tokens() and state(). These access
the token information from the highlighter, and also run the highlighter
if it has not run yet.

If you alter the document and directly after that need the new tokens,
use update().

"""

from __future__ import unicode_literals

from PyQt4.QtGui import QTextCursor

import cursortools
import highlighter


def tokens(block):
    """Returns the tokens for the given block as a (possibly empty) tuple."""
    try:
        return highlighter.userData(block).tokens
    except AttributeError:
        highlighter.highlighter(block.document()).rehighlight()
    try:
        return highlighter.userData(block).tokens
    except AttributeError:
        return ()


def state(blockOrCursor):
    """Returns a thawn ly.lex.State() object at the beginning of the given QTextBlock.
    
    If the argument is a QTextCursor, uses the current block or the first block of its selection.
    
    """
    if isinstance(blockOrCursor, QTextCursor):
        if blockOrCursor.hasSelection():
            block = blockOrCursor.document().findBlock(blockOrCursor.selectionStart())
        else:
            block = blockOrCursor.block()
    else:
        block = blockOrCursor
    if block.userState() == -1:
        highlighter.highlighter(block.document()).rehighlight()
    return highlighter.highlighter(block.document()).state(block)


def update(block):
    """Retokenizes the given block, saving the tokens in the UserData."""
    highlighter.highlighter(block.document()).rehighlightBlock(block)


def cursor(block, token, start=0, end=None):
    """Returns a QTextCursor for the given token in the given block.
    
    If start is given the cursor will start at position start in the token
    (from the beginning of the token). Start defaults to 0.
    If end is given, the cursor will end at that position in the token (from
    the beginning of the token). End defaults to the length of the token.
    
    """
    if end is None:
        end = len(token)
    cursor = QTextCursor(block)
    cursor.setPosition(block.position() + token.pos + start)
    cursor.setPosition(block.position() + token.pos + end, QTextCursor.KeepAnchor)
    return cursor


def selectedTokens(cursor, state=None):
    """Yields block, selected_tokens for every block that has selected tokens.
    
    Usage:
    
    for block, tokens in selectedTokens(cursor):
        for token in tokens:
            do_something() ...
    
    If state is given, it should be the state at the start of the block
    the selection begins. (Use state(cursor) to get that.)
    
    """
    if not cursor.hasSelection():
        return
    d = cursor.document()
    start = d.findBlock(cursor.selectionStart())
    end = d.findBlock(cursor.selectionEnd())
    block = start
    
    if state:
        def token_source():
            for token in tokens(block):
                state.followToken(token)
                yield token
    else:
        def token_source():
            for token in tokens(block):
                yield token
    
    def source_start(source):
        for token in source:
            if token.pos >= cursor.selectionStart() - start.position():
                yield token
    
    def source_end(source):
        for token in source:
            if token.end > cursor.selectionEnd() - end.position():
                break
            yield token
    
    source = source_start(token_source())
    while True:
        if block == end:
            yield block, source_end(source)
            break
        yield block, source
        block = block.next()
        source = token_source()


def allTokens(document):
    """Yields all tokens of a document."""
    return (token for block in cursortools.allBlocks(document) for token in tokens(block))


class TokenIterator(object):
    """An iterator over the tokens in the userData a given QTextBlock."""
    def __init__(self, block, atEnd=False):
        """Positions the token iterator at the start of the given block.
        
        If atEnd == True, the iterator is positioned past the end of the block.
        
        """
        self.block = block
        self._tokens = tokens(block)
        self._index = len(self._tokens) if atEnd else -1
    
    def forward(self, change = True):
        """Yields tokens in forward direction.
        
        If change == True, also advances to the next lines.
        
        """
        while self.block.isValid():
            while self._index + 1 < len(self._tokens):
                self._index += 1
                yield self._tokens[self._index]
            if not change:
                return
            self.__init__(self.block.next())

    def backward(self, change = True):
        """Yields tokens in backward direction.
        
        If change == True, also goes on to the previous lines.
        
        """
        while self.block.isValid():
            while self._index > 0:
                self._index -= 1
                yield self._tokens[self._index]
            if not change:
                return
            self.__init__(self.block.previous(), True)
    
    def forward_state(self, change=True):
        """Returns a token iterator and a state instance.
        
        The iterator yields tokens from beginning of the block.
        The State is the tokenizer state at the same place,
        automatically updated by following the tokens.
        
        If change == True, also advances to the next lines.
        
        """
        state = highlighter.highlighter(self.block.document()).state(self.block)
        def generator():
            for token in self.forward(change):
                state.followToken(token)
                yield token
        return generator(), state

    def token(self):
        """Re-returns the last yielded token."""
        return self._tokens[self._index]
        
    def cursor(self, start=0, end=None):
        """Returns a QTextCursor for the last token.
        
        If start is given the cursor will start at position start in the token
        (from the beginning of the token). Start defaults to 0.
        If end is given, the cursor will end at that position in the token (from
        the beginning of the token). End defaults to the length of the token.
        
        """
        return cursor(self.block, self._tokens[self._index], start, end)

    def copy(self):
        obj = object.__new__(self.__class__)
        obj.block = self.block
        obj._tokens = self._tokens
        obj._index = self._index
        return obj

