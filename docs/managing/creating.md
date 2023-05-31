# Creating new files

## New document

By default, Frescobaldi always creates one empty document, where you can start
right away with typing LilyPond music.

It is recommended to always include the LilyPond version you plan to use for
the document at the top of the file. This way, you can always recognize which
LilyPond version you need to use to compile the document. LilyPond evolves
quite fast, so although efforts are undertaken to not change the basic syntax,
lots of new features and reorganisations of the LilyPond code sometimes
make small changes to the language necessary.

You can use {menu}`snippets -> LilyPond Version` to insert the LilyPond version
you have set as default in the document.

If you want the version always written in any new document you create, you can
enable that in the [](/preferences/index.md). It is even possible to specify any
template as the default one.

## New from template

You can also select {menu}`File -> New from Template` and select a template
there.

A template is simply a snippet that has the `template` variable set.

You can define templates by creating them and then choosing {menu}`File -> Save
as Template`.  You can edit already defined templates using the command
{menu}`File > New from Template -> Manage Templates...`.

## Using the Score Wizard

A third way to create a new document is to use the [Score
Wizard](/getting-started/scorewiz.md).


```{seealso}
snippets
```
