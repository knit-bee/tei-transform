## del-child
Remove `<p/>` elements that are children of `<del/>` by stripping the `<p/>` tag. Children of the `<p/>` element will be added as children of `<del/>` and text and tail at the appropriate position.

### Example
Before transformation:
```xml
<div>
  <p>text1
    <del>text2
      <p>text3</p>text4
      <p>text5</p>text6
    </del>
  </p>
  <p>
    <del>text7
      <p>text8
        <quote>text9</quote>
      </p>
    </del>
  </p>
</div>
```

After transformation:
```xml
<div>
  <p>text1
    <del>text2 text3 text4 text5 text6</del>
  </p>
  <p>
    <del>text7 text8<quote>text9</quote></del>
  </p>
</div>
```
