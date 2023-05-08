## hi-child
Remove `<p/>` elements that are children of `<hi/>` by stripping the `<p/>` tag. Children of the `<p/>` element will be added as children of `<hi/>` and text and tail at the appropriate position.
If the `<hi/>` element contains text and the `<p/>` element also contains text or tail (and no children), an `<lb/>` element is inserted to separate the text parts.

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
    <hi>text10
      <p/>text11
    </hi>
  </p>
</div>
```

After transformation:
```xml
<div>
  <p>text1
    <hi>text2<lb/>text3 text4<lb/>text5 text6</hi>
  </p>
  <p>
    <hi>text7<lb/>text8<hi>text9</hi></hi>
    <hi>text10<lb/>text11</hi>
  </p>
</div>
```
