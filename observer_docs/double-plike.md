## double-plike
Remove  `<p/>` and `<ab/>` that are children of `<p/>`-like elements (i.e. `<p/>` or `<ab/>`) by stripping the inner tag. This will add the children of the inner element as children of the parent and add text and tail of the inner element at the appropriate position. To avoid wrong concatenation of the text content, it will be padded with whitespace before concatenation and multiple whitespace characters will be stripped.

### Example
Before transformation:
```xml
<div>
  <p>text1
    <ab>text2</ab>
    <list/>tail1
    <ab/>tail2
  </p>
</div>
```

After transformation:
```xml
<div>
  <p>text1 text2<list/>tail1 tail2</p>
</div>
```
