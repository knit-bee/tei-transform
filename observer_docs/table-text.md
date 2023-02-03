## table-text
Remove text content from `<table/>` elements and tail on their children and convert `<p/>` children of `<table/>` to `<fw/>`.

Text content of `<table/>` is added to a new `<head/>` element.
Tails of elements are concatenated with the text content of the element or, if the tag is `<row/>`, added to the the content of the last `<cell/>` child.  

### Example
Before transformation:
```xml
<table>
  text
  <row>
    <cell>data</cell>
  </row>tail1
  <row/>tail2
  <p>text2</p>
</table>
```

After transformation:
```xml
<table>
  <head>text</head>
  <row>
    <cell>data tail1</cell>
  </row>
  <row>
    <cell>tail2</cell>
  </row>
  <fw>text2</fw>
</table>
```
