# Document Variables

Document variables are variables that influence the behaviour of Frescobaldi.
They can be written in the first five or last five lines of a document.
If a line contains '`-*-`', Frescobaldi searches the rest of
the lines for variable definitions like `name: value;`.

The following variables are recognized:

## General variables

{samp}`mode: {mode};`
: Force mode to be one of `lilypond`, `html`, `texinfo`, `latex`,
  `docbook` or `scheme`. Default: automatic mode recognition.

{samp}`master: {filename};`
: Compiles another LilyPond document instead of the current.

{samp}`output: {name};`
: Looks for output documents (PDF, MIDI, etc.) starting with
  the specified name or comma-separated list of names.
  [var_output More information].

{samp}`coding: {encoding};`
: Use another encoding than the default UTF-8.

{samp}`version: {version};`
: Set the LilyPond version to use, can be used for non-LilyPond documents.

## Indentation variables

{samp}`tab-width: {number};`
: The visible width of a tab character in the editor, by default 8.

{samp}`indent-tabs: {yes/no};`
: Whether to use tabs in indent, by default `no`.

{samp}`indent-width: {number};`
: The number of spaces each indent level uses, by default 2.
  This value is ignored when `indent-tabs` is set to `yes`.

{samp}`document-tabs: {yes/no};`
: Whether to use tabs elsewhere in the document, by default `no`.

{samp}`document-tab-width: {number};`
: How many spaces to insert when Tab is pressed in the middle of text,
  by default 8. This value is ignored when `document-tabs` is set to `yes`.

```{toctree}
output
```
