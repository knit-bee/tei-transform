## lonely-s
Wrap `<s/>` elements that are children of `<div/>` or `<body/>` with a new `<p/>` element.
Multiple adjacent `<s/>` elements are added to the same `<p/>` element.

### Example
Before transformation:
```xml
<div>
  <s>text1</s>
  <p>text2</p>
  <s>text3</s>
  <s>text4</s>
</div>
```

After transformation:
```xml
<div>
  <p>
    <s>text1</s>
  </p>
  <p>text2</p>
  <p>
    <s>text3</s>
    <s>text4</s>
  </p>
</div>
```
