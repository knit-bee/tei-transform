## hi-child
Remove `<p/>` elements that are children of `<hi/>` by stripping the `<p/>` tag. Children of the `<p/>` element will be added as children of `<hi/>` and text and tail at the appropriate position.

### Example
Before transformation:
```xml
<div>
  <p>text1
    <hi>text2
      <p>text3</p>text4
      <p>text5</p>text6
    </hi>
  </p>
  <p>
    <hi>text7
      <p>text8
        <hi>text9</hi>
      </p>
    </hi>
  </p>
</div>
```

After transformation:
```xml
<div>
  <p>text1
    <hi>text2 text3 text4 text5 text6</hi>
  </p>
  <p>
    <hi>text7 text8<hi>text9</hi></hi>
  </p>
</div>
```
