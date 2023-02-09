## nested-fw
Find `<fw/>` elements with `<fw/>` parent and `<list/>` descendant, where the `<list/>` has in turn  `<fw/>` or `<p/>` as parent, and add the target element as following sibling of the parent.
If the target `<fw/>` element has following siblings, they are added under a new `<fw/>`, which is added as sibling of the target `<fw/>`.
The new `<fw/>` element will be specified with the type or rendition attributes (`@type, @rend, @rendition, @style`) of the parent, if present.
If the parent element is empty after the transformation, it will be removed.
N.B.: Multiple nested `<fw/>` elements are not invalid according to TEI P5. However this plugin should be applied if *fw-child* is used to avoid nesting of `<fw/>` and `<ab/>` elements, since an `<fw/>` element with `<list/>` as child will be converted to `<ab/>` there.

### Example
Before transformation:
```xml
<div>
  <fw rend='h2'>text1
    <fw>text2
      <fw>text3
        <p>
          <list/>
        </p>
      </fw>
    </fw>
    <quote>text4</quote>
  </fw>
  <fw>
    <fw>text5
      <list>
        <item/>
      </list>
    </fw>
  </fw>
</div>
```

After transformation:
```xml
<div>
  <fw rend='h2'>text1</fw>
  <fw>text2</fw>
  <fw>text3
    <p>
    <list/>
    <p/>
  </fw>
  <fw rend='h2'>
    <quote>text4</quote>
  </fw>
  <!-- empty <fw/> parent removed -->
  <fw>text5
    <list>
      <item/>
    </list>
  </fw>
</div>
```
