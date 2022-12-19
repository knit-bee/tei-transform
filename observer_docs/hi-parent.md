## hi-parent
Wrap ```<hi/>``` elements in ```<p/>``` elements if they are not contained by one but direct children of ```<body/>``` or ```<div/>```. If siblings contain any ```<div/>``` element, the new ```<p/>``` is additionally surrounded by a ```<div/>``` (with the according number if the divisions are numbered) to avoid ```<p/>``` and ```<div/>``` on the same level. Empty ```<hi/>``` elements will be removed instead.

### Example
Before transformation:
```xml
<body>
  <hi>some highlighted text</hi>
  <div>
    <hi>Header</hi>
    <p>more text</p>
  </div>
</body>
```

After transformation:
```xml
<body>
  <div>
    <p>
      <hi>some highlighted text</hi>
    </p>
  </div>
  <div>
    <p>
      <hi>Header</hi>
    </p>
    <p>more text</p>
  </div>
</body>
```
