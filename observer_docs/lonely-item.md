## lonely-item
Find `<item/>` elements that are outside `<list/>` elements and add a new `<list/>` as parent.
Empty `<item/>` elements are removed. If the `<item/>` element has a tail, it will be removed and added to the text content of `<item/>` or concatenated with the tail of its last child, if present.
Multiple adjacent elements are gathered under the same `<list/>` element.
N.B.: The inner element of nested `<item/>` elements will be ignored, use *double-item* plugin to resolve this structure.
### Example
Before transformation:
```xml
<div>
  <p>
    <item>text1</item>
    <item>text2</item>
    <item/>
  </p>
  <item>
    <p>text3</p>
  </item>tail1
  <item/>tail2
  <p>more text</p>
  <item>
    <item>text</item>
  </item>
</div>
```

After transformation:
```xml
<div>
  <p>
    <list>
      <item>text1</item>
      <item>text2</item>
    <list/>
  </p>
  <list>
    <item>
      <p>text3</p>tail1
    </item>
    <item>tail2</item>
  </list>
  <p>more text</p>
  <list>
    <item>
      <!-- invalid item in item: use double-item plugin to resolve-->
      <item>text</item>
    </item>
  </list>
</div>
```
