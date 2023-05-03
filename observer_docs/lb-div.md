## lb-div
Wrap `<lb/>` elements that are children of `<div/>` or `<body/>` and have tail with a new `<p/>` element.
Multiple adjacent `<lb/>` will be added to the same `<p/>` element.

### Example
Before transformation:
```xml
<div>
  <lb/>tail1
  <lb/>tail2
  <p>text</p>
  <lb/>tail3
  <lb/>
</div>
```

After transformation:
```xml
<div>
  <p>
    <lb/>tail1
    <lb/>tail2
  </p>
  <p>text</p>
  <p>
    <lb/>tail3
  </p>
  <lb/>
</div>
```
