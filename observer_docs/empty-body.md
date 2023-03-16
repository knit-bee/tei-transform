## empty-body
Add empty `<p/>` to `<body/>` elements without (required) children, i.e. it is missing an element from [model.common](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-model.common.html) or a `<div/>` element.
If the `<body/>` element contains text, use *body-text* plugin to remove it.


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
          <body>
            <head>text1</head>
          </body>
        </floatingText>
      </div>
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
            <head>text1</head>
            <p/>
          </body>
        <floatingText>
      </div>
      <div>
        <floatingText>
          <body>text1
            <p/>
          </body>
        </floatingText>
      </div>
    </body>
  </text>
</TEI>
```
