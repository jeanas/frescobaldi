# Snippets

With the snippets manager you can store often used pieces of text called
"snippets", and easily paste them into the text editor.

The snippets manager can be activated via the menu {menu}`snippets`.

Snippets can be searched by browsing the list or by typing some characters
in the search entry.
Snippets can also have keyboard shortcuts applied to them.
Some snippets have a special mnemonic (short name) which you can also type
in the search entry to select the snippet. Pressing the Return key will then
apply the snippet to the text editor and hide the snippets manager.

Add new snippets using {kbd}`INS`. Edit the selected snippet with {kbd}`F2`.
Remove selected snippets using {kbd}`Ctrl+DEL`. Warning: this cannot be undone!

Snippets can also be put in the menu (see [](snippet-editor/index.md)).  And
finally, there are snippets which can include or alter selected text.  Some
snippets do this by using special variables, while others are small scripts
written in Python.


```{toctree}
snippet-editor/index
snippet-lib
snippet-import-export
```
