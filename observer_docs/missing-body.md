## missing-body
Add a `<body/>` element to `<text/>` elements that do not have a  `<body/>` or `<group/>` element as child. All children of the `<text/>` element are moved to the `<body/>` element, apart from `<front/>` or `<back/>` elements.
The `<body/>` element is inserted as first child of the `<text/>` element or after the `<front/>` element, if present.
If the new `<body/>` element doesn't have any children, a new, empty `<p/>` element is added to avoid this invalid structure.

### Example
Before transformation:
```xml
<TEI>
  <teiHeader/>
  <text>
    <group>
      <text>
        <front/>
        <p>text</p>
        <back/>
      </text>
      <text>
        <p>text2</p>
        <back/>
      </text>
      <text>
        <front/>
        <back/>
      </text>
    </group>
  </text>
</TEI>
```

After transformation:
```xml
<TEI>
  <teiHeader/>
  <text>
    <group>
      <text>
        <front/>
        <body>
          <p>text</p>
        </body>
        <back/>
      </text>
      <text>
        <body>
          <p>text2</p>
        </body>
        <back/>
      </text>
      <text>
        <front/>
        <body>
          <p/>
        </body>
        <back/>
      </text>
    </group>
  </text>
</TEI>

```
