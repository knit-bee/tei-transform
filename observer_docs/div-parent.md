## div-parent
Handle `<div/>` elements with invalid parent elements (e.g. every tag that is not `<body/>`, `<front/>`, `<back/>`, `<div/>`, `<lem/>`, or `<rdg/>`).

If the tag of the parent is `<p/>` or `<ab/>`, the parent tag will be converted to `<div/>`.

For every other parent tag, the invalid  `<div/>` element is stripped from the tree by merging its children, text and tail into the parent.

If the `<div/>` element is empty, it will be removed.

N.B.: Use the appropriate other plugins in combination with *div-parent* to avoid an invalid tree that might result from this transformation, e.g. *p-div-sibling*, *div-text*, *tail-text* etc.


### Example
Before transformation:
```xml
<div>
  <p>
    <div/>
  </p>
  <p>
    <div>
      <p>text</p>
    </div>
  </p>
  <list>
    <item>
      <div>
        <p>text</p>
      </div>
    </item>
  </list>
</div>
```

After transformation:
```xml
<div>
  <p/> <!-- empty <div/> removed -->
  <div>
    <div>
      <p>text</p>
    </div>
  </div>
  <list> <!-- use other plugin to resolve wrong siblings  -->
    <item>
        <p>text</p>
    </item>
  </list>
</div>
```
