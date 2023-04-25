## head-parent
Change tag of `<head/>` elements that are children of `<p/>`, `<ab/>`, `<hi/>`, `<head/>`, or `<item/>` to `<hi/>`.

### Example
Before transformation:
```xml
<div>
  <p>text1<head>text2</head></p>
  <list>
    <item>
      <head>text3
        <head>text4</head>
      </head>
    </item>
  </list>
</div>
```

After transformation:
```xml
<div>
  <p>text1<hi>text2</hi></p>
  <list>
    <item>
      <hi>text3
        <hi>text4</hi>
      </hi>
    </item>
  </list>
</div>
```
