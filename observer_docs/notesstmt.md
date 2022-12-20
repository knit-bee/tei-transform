## notesstmt
Remove ```@type``` from ```<notesStmt/>```, as it is not a valid attribute on this element.

### Example
Before transformation:
```xml
<teiHeader>
  <!--  ... -->
  <noteStmt type="value">
    <note/>
  </noteStmt>
  <!-- ... -->
</teiHeader>
```

After transformation:
```xml
<teiHeader>
  <!--  ... -->
  <noteStmt>
    <note/>
  </noteStmt>
  <!-- ... -->
</teiHeader>
```
