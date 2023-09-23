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
These functions return values for python format variables in user guide pages.

Some generic functions are called by several pages, but there are also some
special, auto-generated parts of text that are used in a specific user
guide page.

"""


import appinfo


## TODO
def snippet_editor_expander():
    """Return the auto-generated list of docstrings of the snippet variables."""
    from snippet import expand
    text = []
    text.append("<dl>")
    text.extend(map("<dt><code>${0[0]}</code></dt><dd>{0[1]}</dd>".format,
                    expand.documentation(expand.Expander)))
    text.append("</dl>")
    return ''.join(text)
