## row-child
Wrap `<p/>` elementst that are direct descendants of `<row/>` in a new `<cell/>` element. If the `<p/>` element does not contain (non-whitespace) text, tail or children, it is removed instead. If the parent `<row/>` would be empty after the removal, and new, empty `<cell/>` is added to the `<row/>`.

### Example
Before transformation:
```xml
<table>
  <row>
    <cell>text</cell>
    <p>  </p>
    <p>text2</p>
  </row>
  <row>
    <p/>
  </row>
</table>
```

After transformation:
```xml
<table>
  <row>
    <cell>text</text>
    <cell>
      <p>text2</p>
    </cell>
  </row>
  <row>
    <cell/>
  </row>
</table>
```
