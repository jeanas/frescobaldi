# Using Extensions

Obviously the actual usage of an extension is up to the extension, and so is the
documentation of its features. However, there are some common aspects about the
integration of extensions in the Frescobaldi user interface. Essentially an
extension's functionality is available through *Menu Actions* and a *Tool
Panel*. At least one of these must exist for any extension.

## Menus

An extension's *Menu Actions* can be exposed in various submenus. It is up to
the extension maintainer(s) which actions are available in each of the following
places:

* {menu}`Tools -> Extensions`
* Editor context menu
* Musicview context menu
* Manuscriptview context menu
* *Additional places may be added over time*

## Tool Panel

If an extensions provides a Tool Panel it is accessible through a panel under
{menu}`Tools -> Extensions`.  The panel behaves like Frescobaldi's built-in
dockable panels, and what functionality it provides is up to the extension.
