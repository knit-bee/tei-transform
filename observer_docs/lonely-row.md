## lonely-row
Find `<row/>` elements that are not a direct descendant of `<table/>` and add a new `<table/>` element as parent. Adjacent `<row/>` elements will be added to the same `<table/>` element. If the `<row/>` element is empty (i.e. doesn't have descendants, text, or tail), it is removed instead of wrapping it in a `<table/>` element.
If the `<row/>` element has a tail, the tail is moved to the `<table/>` parent element or, if already existing, concatenated with the tail of the parent.


### Example
Before transformation:
```xml
<div>
  <p>
    <row>
      <cell>text</cell>
    </row>
    <row>
      <cell>text2</cell>
      <cell>text3</cell>
    </row>tail
  </p>
  <row/>
  <row>
    <cell>new table</cell>
  </row>
</div>
```

After transformation:
```xml
<div>
  <p>
    <table>
      <row>
        <cell>text</cell>
      </row>
      <row>
        <cell>text2</cell>
        <cell>text3</cell>
      </row>
    </table>tail
  </p>
  <table>
    <row>
      <cell>new table</cell>
    </row>
  </table>
</div>
```
