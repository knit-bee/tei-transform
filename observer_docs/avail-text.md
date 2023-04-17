## avail-text
Remove text content from ```<availability/>``` elements and tail of children of `<availability/>`. The text is added as content of a new `<p/>` element that is inserted at the appropriate index.

### Example
Before transformation:
```xml
<teiHeader>
  <publicationStmt>
    <publisher/>
    <date/>
    <availability>text
      <p>text2</p>tail
      <licence>text3</licence>tail2
    </availability>
  </publicationStmt>
</teiHeader>
```

After transformation:
```xml
<teiHeader>
  <publicationStmt>
    <publisher/>
    <date/>
    <availability>
      <p>text</p>
      <p>text2</p>
      <p>tail</p>
      <licence>text3</licence>
      <p>tail2</p>
    </availability>
  </publicationStmt>
</teiHeader>
```
