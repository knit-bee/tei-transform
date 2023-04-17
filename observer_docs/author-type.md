## author-type
Handle attribute ```@type``` of ```<author/>``` elements. The default transformation will remove the attribute.
This plugin can be configured to replace the attribute's name with `@role`. To do so, include the following section in the config file:

```
[author-type]
action=replace
```

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
