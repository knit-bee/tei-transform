## double-plike
Remove  `<p/>` and `<ab/>` that are children of `<p/>`-like elements (i.e. `<p/>` or `<ab/>`) by stripping the inner tag. This will add the children of the inner element as children of the parent and add text and tail of the inner element at the appropriate position. To avoid wrong concatenation of the text content, it will be padded with whitespace before concatenation and multiple whitespace characters will be stripped.

This plugin can be configured to insert an `<lb/>` element between the text of the parent or the tail of the older sibling and the text content of the target element that would otherwise be concatenated to one part. To do so, include the following section in the config file:
```
[double-plike]
action=add-lb
```

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

a. without configuration
```xml
<div>
  <p>text1 text2<list/>tail1 tail2</p>
</div>
```

b. with configuration
```xml
<div>
  <p>text1
    <lb/>text2
    <list/>tail1
    <lb/>tail2
  </p>
</div>
```
