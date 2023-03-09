## body-text
Remove text from ```<body/>``` elements and add under new ```<p/>```.

N.B.: Tails on child elements of `<body/>` are not handled. Use in combination with *p-head* to avoid `<head/>` elements after `<p/>`, e.g. if the first child of `<body/>` is `<head/>`.

### Example
Before transformation:
```xml
<TEI>
  <teiHeader/>
  <text>
    <body>text1
      <div>
        <p>some text</p>
      </div>
  </body>
</text>
</TEI>
```

After transformation:
```xml
<TEI>
  <teiHeader/>
  <text>
    <body>
      <p>text1</p>
      <div>
        <p>some text</p>
      </div>
  </body>
</text>
</TEI>
```
