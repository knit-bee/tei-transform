## u-parent
Handle `<u/>` elements with `<p/>` as parent by changing the tag of the parent to `<div/>`. If the parent contains text, a new `<p/>` is added as first child containing the text content.
If the target element has a tail, it is merged with its text content or added to the tail of the last child, if present.
If the `<u/>` element is empty, it is removed instead.

### Example
Before transformation:
```xml
<body>
  <p>text1
    <u>text2</u>tail
  </p>
  <p>
    <u>text3<hi>text4</hi></u>tail2
  </p>
</body>
```

After transformation:
```xml
<body>
  <div>
    <p>text1</p>
    <u>text2 tail</u>
  </div>
  <div>
    <u>text3<hi>text4</hi>tail2</u>
  </div>
</body>
```
