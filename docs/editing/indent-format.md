# Indentation and Formatting

By default, Frescobaldi will automatically indent two spaces after
characters such as `{` and `<<`. This is in accordance with the indenting
the LilyPond documentation uses.

You can change the indenting behaviour by using [docvars document variables].
In the following example, Frescobaldi will use 4 spaces for indent.

```
% -*- indent-width: 4;
\relative {
    c2 d4 e8 f16 r
}
```

You can also change the default behaviour of Frescobaldi in the [editor
preferences](/preferences/editor.md).

Besides indenting, Frescobaldi is also able to align indented lines with
other characters on the previous line, after the character that starts the
indent. Consider the following example:

```
\relative {
  << { c d e f g }
     { e f g a b } >>
  d2.
}
```

The line `{ e f g a b }` aligns itself with the preceding construct,
regardless of the indent-with currently in use.
