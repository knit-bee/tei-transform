## row-child
Wrap `<p/>` elementst that are direct descendants of `<row/>` in a new `<cell/>` element. If the `<p/>` element does not contain (non-whitespace) text, tail or children, it is removed instead.

### Example
Before transformation:
```xml
<table>
  <row>
    <cell>text</cell>
    <p>  </p>
    <p>text2</p>
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
</table>
```
