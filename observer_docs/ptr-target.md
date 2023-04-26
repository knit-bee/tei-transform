## ptr-target
Remove `@target` attribute from `<ptr/>` elements if the value is empty.

### Example
Before transformation:
```xml
<publicationStmt/>
  <publisher/>
  <ptr target=""/>
</publicationStmt>
```

After transformation:
```xml
<publicationStmt/>
  <publisher/>
  <ptr/>
</publicationStmt>
```
