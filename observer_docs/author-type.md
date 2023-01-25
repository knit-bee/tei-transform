## author-type
Remove attribute ```@type``` from ```<author/>``` elements. N.B.: The ```@type``` attribute is not valid on ```<author/>``` elements and should be removed.

### Example
Before transformation:
```xml
<titleStmt>
  <author type="something">Name</author>
  <title/>
</titleStmt>
```

After transformation:
```xml
<titleStmt>
  <author>Name</author>
  <title/>
</titleStmt>
```
