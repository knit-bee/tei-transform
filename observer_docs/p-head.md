## p-head
Replace ```<head/>``` tags that appear after ```<p/>``` with ```<ab/>``` and add ```@type="head"``` attribute.

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
