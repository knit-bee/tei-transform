## invalid-role
Remove `@role` attribute from `<p/>` and `<div/>` elements.

### Example
Before transformation:
```xml
<body>
  <div role='content' type='sth'>
    <p role='value'>text</p>
  </div>
</body>
```

After transformation:
```xml
<body>
  <div type='sth'>
    <p>text</p>
  </div>
</body>
```
