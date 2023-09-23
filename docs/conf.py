from pathlib import Path
import sys

# Allow to find extensions in ext/
sys.path.insert(0, str(Path(__file__).parent / "sphinx-extensions"))

html_title = "Frescobaldi User Guide"

extensions = [
    # MyST extension for using Sphinx with Markdown (instead of reStructuredText)
    "myst_parser",
    # Custom extension for Frescobaldi-specific markup (lives in ext/)
    "frescobaldi_markup",
]
# MyST Markdown syntax extensions
myst_enable_extensions = [
    # Definition lists
    "deflist",
    # Automatically turn inline URLs into hyperlinks
    "linkify"
]

# LilyPond is the default syntax highlighting language for code blocks.
highlight_language = "lilypond"
# Since LilyPond has specific Pygments tokens, it must always be used
# with the "LilyPond" style.
pygments_style = "lilypond"

locale_dirs = ["../frescobaldi_app/i18n"]
gettext_compact = "userguide"

html_theme = "nature"
html_use_index = False
html_copy_source = False
html_show_copyright = False
html_show_sphinx = False
html_sidebars = {"**": []} # remove default sidebar
