## head-type
Remove attribute ```@type``` from ```<head/>``` elements. N.B.: The ```@type``` attribute is not invalid on ```<head/>``` elements.

### Example
Before transformation:
```xml
<div>
  <head type="something">Header</head>
  <p/>
</div>
```

After transformation:
```xml
<div>
  <head>Header</head>
  <p/>
</div>
```
