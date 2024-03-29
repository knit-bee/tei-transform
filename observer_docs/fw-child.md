## fw-child
Handle `<p/>`, `<list/>`, and `<table/>` elements with `<fw/>` parent.
Remove `<p/>` elements with `<fw/>` parent by stripping the `<p/>` element. Text, tail, and children of the `<p/>` element are merged into the parent. The text parts will be concatenated and separated by one whitespace. Formatting whitespace from text and tail will be removed.

For `<list/>` or `<table/>` elements in `<fw/>`, the parent tag is changed to `<ab/>`.

N.B.:
- Use in combination with *double-plike* if `<list/>` and `<p/>` are siblings in `<fw/>`.
- Use in combination with *nested-fw* to avoid nesting of `<fw/>` and `<ab/>`.


### Example
Before transformation:
```xml
<div>
  <fw>text1
    <p>text2</p>text3
  </fw>
  <fw>
    <list>
      <item/>
    </list>
  </fw>
  <fw>
    <list>
      <item/>
    </list>
    <p>text</p>
  </fw>
  <fw>
    <table>
      <row>
        <cell>text</cell>
      </row>
    </table>
  </fw>
</div>
```

After transformation:
```xml
<div>
  <fw>text1 text2 text3</fw>
  <ab>
    <list>
      <item/>
    </list>
  </ab>
  <ab>
    <list>
      <item/>
    </list>
    <!-- use double-plike plugin to resolve this-->
    <p>text</p>
  </ab>
  <ab>
    <table>
      <row>
        <cell>text</cell>
      </row>
    </table>
  </ab>
</div>
```
