## div-tail
Remove tail on `<div/>` elements and add as text content of a new `<p/>` that is inserted as last child of the `<div/>`.
N.B.: Use in combination with *p-div-sibling* plugin to avoid `<p/>` following `<div/>` structure.

### Example
Before transformation:
```xml
<body>
  <div>
    <div>
      <p>text</p>
    </div>tail1
  </div>tail2
</body>
```

After transformation:
```xml
<body>
  <div>
    <div>
      <p>text</p>
      <p>tail1</p>
    </div>
    <p>tail2</p> <!--  use p-div-sibling to resolve this -->
  </div>
</body>
```
