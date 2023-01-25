## code-elem
Find  `<code/>` elements that have children or that are direct descendants of `<div/>` elements and change their tag to `<ab/>`.
N.B.: Use in combination with *double-plike* plugin to avoid nesting of `<p/>` and `<ab/>`.

### Example
Before transformation:
```xml
<div>
  <code>abc</code>
  <p>
    <code>
      <hi>text</hi>
    </code>
  </p>
</div>
```

After transformation:
```xml
<div>
  <ab>abc</ab>
  <p>
    <!-- use double-plike to avoid this invalid structure -->
    <ab>
      <hi>text</hi>
    </ab>
  </p>
</div>
```
