## misp-notesstmt
Insert `<notesStmt/>` elements that have `<sourceDesc/>` as previous sibling before the `<sourceDesc/>` element.

### Example
Before transformation:
```xml
<fileDesc>
  <titleStmt/>
  <publicationStmt/>
  <seriesStmt/>
  <sourceDesc/>
  <notesStmt>
    <note/>
  </notesStmt>
</fileDesc>
```

After transformation:
```xml
<fileDesc>
  <titleStmt/>
  <publicationStmt/>
  <seriesStmt/>
  <notesStmt>
    <note/>
  </notesStmt>
  <sourceDesc/>
</fileDesc>
```
