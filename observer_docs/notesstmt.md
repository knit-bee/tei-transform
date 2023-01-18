## notesstmt
Remove ```@type``` from ```<notesStmt/>```, as it is not a valid attribute on this element.

### Example
Before transformation:
```xml
<teiHeader>
  <!--  ... -->
  <notesStmt type="value">
    <note/>
  </notesStmt>
  <!-- ... -->
</teiHeader>
```

After transformation:
```xml
<teiHeader>
  <!--  ... -->
  <notesStmt>
    <note/>
  </notesStmt>
  <!-- ... -->
</teiHeader>
```
