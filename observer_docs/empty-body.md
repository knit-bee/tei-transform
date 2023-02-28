## empty-body
Add empty `<p/>` to `<body/>` elements without children. If the `<body/>` element contains text, the text is added to the new `<p/>` and removed from the `<body/>` element.


### Example
Before transformation:
```xml
<TEI>
  <teiHeader/>
  <text>
    <body/>
  </text>
  <text>
    <body>
      <div>
        <floatingText>
          <body>text1</body>
        </floatingText>
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
      <p/>
    </body>
  </text>
  <text>
    <body>
      <div>
        <floatingText>
          <body>
            <p>text1</p>
          </body>
        <floatingText>
      </div>
    </body>
  </text>
</TEI>
```
