"""Implement the {menu}`...` role.

It works like {menu}`Edit -> Preferences` and translates the individual menu
parts automatically.
"""

from docutils import nodes
from sphinx.util.docutils import SphinxRole

from frescobaldi_app import toplevel
toplevel.install()
import i18n
import qutil

class Menu(SphinxRole):
    def get_title(self, name):
        standard_names = {
            # untranslated standard menu names
            "file": "menu title|&File",
            "edit": "menu title|&Edit",
            "view": "menu title|&View",
            "snippets": "menu title|Sn&ippets",
            "music": "menu title|&Music",
            "lilypond": "menu title|&LilyPond",
            "tools": "menu title|&Tools",
            "window": "menu title|&Window",
            "session": "menu title|&Session",
            "help": "menu title|&Help",
        }
        try:
            name = standard_names[name]
        except KeyError:
            pass
        if name.startswith("!"):
            remove_accel = False
            name = name[1:]
        else:
            remove_accel = True
        try:
            ctxt, msg = name.split("|", 1)
        except ValueError:
            translation = _(name)
        else:
            translation = _(ctxt, msg)
        if remove_accel:
            translation = qutil.removeAccelerator(translation).strip(".")
        return translation

    def run(self):
        pieces = [name.strip() for name in self.text.split("->")]
        translated = [self.get_title(name) for name in pieces]
        arrow = " \u2192 "
        full_text = arrow.join(translated)
        return ([nodes.emphasis("", full_text)], [])

def setup(app):
    app.add_role("menu", Menu())
    # Here, unlike the normal Frescobaldi application, we set up
    # internationalization with the language that the documentation is being
    # built in, not the system / user-preferred language.
    i18n.install(app.config.language)
