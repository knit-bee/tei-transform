## schemaLocation
Remove ```@schemaLocation``` attribute from ```<TEI/>```elements.

### Example
Before transformation:
```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="some//location">
  <teiHeader>
  <!-- ... -->
</TEI>
```

After transformation:
```xml
<TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <teiHeader>
  <!-- ... -->
</TEI>
```
