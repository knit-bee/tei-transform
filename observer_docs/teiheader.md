## teiheader
Remove ```@type``` attribute from ```<teiHeader/>```.

### Example
Before transformation:
```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader type="value">
    <!-- ... -->
```

After transformation:
```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <!-- ... -->
```
