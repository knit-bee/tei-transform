## lonely-row
Find `<row/>` elements that are not a direct descendant of `<table/>` and add a new `<table/>` element as parent. Adjacent `<row/>` elements will be added to the same `<table/>` element. If the `<row/>` element is empty (i.e. doesn't have descendants, text, or tail), it is removed instead of wrapping it in a `<table/>` element.
If the `<row/>` element has a tail, the tail is moved to the last `<cell/>` element or, if `<row/>` has no children, a new `<cell/>` is added containg the tail.


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
        <cell>text3 tail</cell>
      </row>
    </table>
  </p>
  <table>
    <row>
      <cell>new table</cell>
    </row>
  </table>
</div>
```
