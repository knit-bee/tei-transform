## table-child
Change tags of `<p/>` elements that are direct children of `<table/>` to `<fw/>`.
N.B.: Use in combination with *table-text* to remove tails of invalid children of `<table/>`.


### Example
Before transformation:
```xml
<table>
  <row>
    <cell/>
  </row>
  <p>text</p>
  <row/>
</table>
```

After transformation:
```xml
<table>
  <row>
    <cell/>
  </row>
  <fw>text</fw>
  <row/>
</table>
```
