# The Music View

The Music View displays the PDF document created by LilyPond.

When LilyPond was run in preview mode (i.e. with Point & Click turned on),
the PDF contains a clickable link for every music object, pointing to its
definition in the text document.

The Music View uses this information to provide smart, two-way integration
with the text document:

* Move the mouse pointer over music objects to highlight them in the text
* Click an object to move the text cursor to that object
* Shift-click an object to edit its text in a small window (see
  [](/editing/edit-in-place.md))
* Move the text cursor to highlight them in the music view, press {menu}`view ->
  &Jump to Cursor Position` to scroll them into view.

You can also adjust the view:

* Use the Control (or Command) key with the mouse wheel to zoom in and out
* Hold Control or Command and left-click to display a magnifier glass
* Configure the background color under {menu}`Edit -> Preferences -> Fonts &
  Colors -> Base Colors -> Background`.

You can copy music right from the PDF view to a raster image: Hold Shift and
drag a rectangular selection (or use the right mouse button) and then select
{menu}`Edit -> Copy to Image...` to copy the selected music as a raster image to
the clipboard, a file or another application.

```{seealso} [](/editing/edit-in-place.md)
```
