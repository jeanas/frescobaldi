# Lyrics

Frescobaldi can automatically place hyphens '` -- `' inside texts to make those
texts usable as lyrics. It can use hyphenation dictionaries of OpenOffice.org,
Scribus, etc.

To use this feature you must first select the text you want to hyphenate. Then
choose {menu}`Tools -> Lyrics -> Hyphenate Lyrics Text...`.  In the dialog that
appears, select the language.  Click OK or press Enter to have the hyphenation
take place.

A small limitation is that word processor hyphenation dictionaries often don't
want to break a word right after the first letter (e.g. '`a -- men`'), because
that does not look nice in word processor texts. So it can happen that you have
to add some hyphens after the first letter of such lyrics.

There is also a command to remove hyphenation. This can be useful if you have a
stanza of lyrics that you just want to display as a markup below the music.
Under {menu}`Edit -> Preferences... -> Paths` you can enter a list of
directories to search for hyphenation pattern files.