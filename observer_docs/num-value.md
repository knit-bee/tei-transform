## num-value
Change attribute `@value` on `<num/>` elements to `@type` if the value is `percent`.

### Example
Before transformation:
```xml
<p>text
  <num value='percent'>20</num>
</p>
```

After transformation:
```xml
<p>text
  <num type='percent'>20</num>
</p>
```
