## p-pubstmt
Remove empty `<p/>` or `<ab/>` elements from `<publicationStmt/>` if there are siblings that are not p-like but from [*model.publicationStmtPart.agency*](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-model.publicationStmtPart.agency.html) or [*model.publicationStmtPart.detail*](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-model.publicationStmtPart.detail.html), i.e. `<publisher/>` etc.
d
If the target element is not empty, no transformation is performed and the observer will raise an error since the file in question requires manual inspection and curation. Check the log file for such errors.

### Example
Before transformation:
```xml
<teiHeader>
  <fileDesc>
    <!-- ... -->
    <publicationStmt>
      <publisher>Name</publisher>
      <p/>
      <date>2023</date>
      <p>text</p>
    </publicationStmt>
  </fileDesc>
</teiHeader>
```

After transformation:
```xml
<teiHeader>
  <fileDesc>
    <!-- ... -->
    <publicationStmt>
      <publisher>Name</publisher>
      <date>2023</date>
      <p>text</p> <!-- Can't be removed without information loss, handle manually -->
    </publicationStmt>
  </fileDesc>
</teiHeader>
```
