## id-attribute
Replace ```@id``` attributes with ```@xml:id``` by adding xml namespace prefix (i.e. 'http://www.w3.org/XML/1998/namespace'). If the node containing the attribute is the ```<TEI/>``` root, the attribute is removed.

### Example
Before transformation:
```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0" id="some value">
  <publicationStmt>
    <publisher id="some id">Publisher</publisher>
  <!-- ... -->
  </publicationStmt>
  <!-- ... -->
</TEI>
```

After transformation:
```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <publicationStmt>
    <publisher xml:id="some id">Publisher</publisher>
  <!-- ... -->
  </publicationStmt>
  <!-- ... -->
</TEI>
```
