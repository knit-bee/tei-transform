## filename-element
Remove ```<filename/>``` elements. ```<filename/>``` is not a valid TEI tag name, if the information contained in this element should be remain in the document, use for instance ```<idno/>``` in a correct environment.

### Example
Before transformation:
```xml
<!-- ... -->
<teiHeader>
  <fileDesc>
    <!-- ... -->
    <sourceDesc/>
    <filename>invalid_tei_file.xml</filename>
  </fileDesc>
   <!-- ... -->
</teiHeader>
<!-- ... -->
```

After transformation:
```xml
<!-- ... -->
<teiHeader>
  <fileDesc>
    <!-- ... -->
    <sourceDesc/>
  </fileDesc>
   <!-- ... -->
</teiHeader>
<!-- ... -->
```
