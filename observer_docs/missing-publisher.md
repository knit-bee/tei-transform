## missing-publisher
Add an empty ```<publisher/>``` element to ```<publicationStmt/>``` if no element from the *publicationStmtPart.agency* group (i.e. ```<publisher/>```, ```<distributor/>```, ```<authority/>```) is present. ```<publicationStmt/>``` should contain as first child an element with one of these tags.
This change will only add the empty ```<publisher/>``` element as first child of  ```<publicationStmt/>```, it will not guarantee that the order of the elements in  ```<publicationStmt/>``` is valid if any element from the *publicationStmtPart.agency* group is found.

### Example
Before transformation:
```xml
<teiHeader>
  <!-- ... -->
  <publicationStmt>
    <address>
      <addrLine>Address</addrLine>
    </address>
    <date>2022-20-20</date>
  </publicationStmt>
    <!-- ... -->
</teiHeader>
```

After transformation:
```xml
<teiHeader>
  <!-- ... -->
  <publicationStmt>
    <publisher/>
    <address>
      <addrLine>Address</addrLine>
    </address>
    <date>2022-20-20</date>
  </publicationStmt>
    <!-- ... -->
</teiHeader>
```
