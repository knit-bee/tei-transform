## rel-item
Remove ```<relatedItem/>``` elements that do not have children (i.e. only contain text) or do not have ```@target``` attribute. If the parent element of ```<relatedItem/>``` would be empty after removal, it will also be removed.

### Example
Before transformation:
```xml
<teiHeader>
  <!-- ... -->
  <biblFull>
    <!-- ... -->
    <notesStmt>
      <note/>
      <relatedItem>content</relatedItem>
    </notesStmt>
  </biblFull>
  <!-- ... -->
</teiHeader>
```

After transformation:
```xml
<teiHeader>
  <!-- ... -->
  <biblFull>
    <!-- ... -->
    <notesStmt>
      <note/>
    </notesStmt>
  </biblFull>
  <!-- ... -->
</teiHeader>
```
