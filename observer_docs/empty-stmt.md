## empty-stmt
Remove `<notesStmt/>` and `<seriesStmt/>` that don't have any children.

### Example
Before transformation:
```xml
<teiHeader>
  <fileDesc>
    <titleStmt/>
    <publicationStmt/>
    <seriesStmt/>
    <notesStmt>
      <note>text</note>
    </notesStmt>
    <notesStmt/>
  </fileDesc>
</teiHeader>
```

After transformation:
```xml
<teiHeader>
  <fileDesc>
    <titleStmt/>
    <publicationStmt/>
    <notesStmt>
      <note>text</note>
    </notesStmt>
  </fileDesc>
</teiHeader>
```
