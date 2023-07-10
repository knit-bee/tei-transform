## code-elem
Find  `<code/>` elements that have children and change their tag to `<ab/>` and set `@type='code'` attribute If the `@type` attribute is already present, it won't be overwritten.
If the `<code/>` element has `@lang` attribute, it is removed and its value is concatenated with the `@type` attribute (only if it was newly set to `code`).
If the parent of the `<code/>` element has tag `<p/>` or `<ab/>`, the `<code/>` element is added as next sibling of its parent during the transformation. Any following siblings are added as children are appended to a new element with the tag of the parent which is added next to the `<code/>` element.  
Use in combination with *double-plike* to avoid nesting of `<ab/>` and `<p/>`, if  the `<code/>` element contains `<p/>` children. If necessary, configure *double-plike* plugin to add `<lb/>` in order to preserve lines in the former `<code/>` element.





### Example
Before transformation:
```xml
<div>
  <code lang='python'>
    for i in range(10):<lb/>
        print(i)
  </code>
  <p>text
    <code>
      <hi>text1</hi>
    </code>
    <list/>
  </p>
</div>
```

After transformation:
```xml
<div>
  <ab type="code-python">
    for i in range(10):<lb/>
        print(i)
  </ab>
  <p>text</p>
  <ab type="code">
    <hi>text1</hi>
  </ab>
  <p>
    <list/>
  </p>
</div>
```
