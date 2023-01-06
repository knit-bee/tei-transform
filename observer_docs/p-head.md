## p-head
Replace ```<head/>``` tags that have older siblings that are not part of 'model.divWrapper' class or `<fw/>` with ```<ab/>``` and add ```@type="head"``` attribute. If the original `<head/>` element is empty (e.g. not containing children or non-whitespace text or tail), the element is removed.

### Example
Before transformation:
```xml
<div>
  <head>header1</head>
  <p>text</p>
  <head>subheading</head>
  <p>more text</p>
</div>
```

After transformation:
```xml
<div>
  <head>header1</head>
  <p>text</p>
  <ab type="head">subheading</ab>
  <p>more text</p>
</div>
```
