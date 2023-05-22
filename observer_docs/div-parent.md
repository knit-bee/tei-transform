## div-parent
Handle `<div/>` elements with invalid parent elements (e.g. every tag that is not `<body/>`, `<front/>`, `<back/>`, `<div/>`, `<lem/>`, or `<rdg/>`).

If the tag of the parent is `<p/>` or `<ab/>` and the `<div/>` element has descendants, the `<div/>` element is added as a sibling of its parent. Any following siblings of the target `<div/>` will also be added after under a new element with the same tag as their former parent and a new `<div/>`, which is added as sibling of the target `<div/>`.
If the `<div/>` has a tail, it is added as text content of a new `<p/>`, which is appended to the target `<div/>`.

For every other parent tag or if the `<div/>` element has no descendants, the invalid  `<div/>` element is stripped from the tree by merging its children, text and tail into the parent.

If the `<div/>` element is empty, it will be removed.

N.B.: Use the appropriate other plugins in combination with *div-parent* to avoid an invalid tree that might result from this transformation, e.g. *div-sibling*, etc.


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
    </div>tail
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
      <p>tail</p>
    </div>
  </div>
  <list> <!-- use other plugin to resolve wrong siblings  -->
    <item>
        <p>text</p>
    </item>
  </list>
</div>
```
