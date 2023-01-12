## lonely-cell
Find  `<cell/>` elements that are outside of a `<row/>` element and wrap them in `<row/>` and `<table/>`, if necessary.
Adjacent `<cell/>` elements will be added to the same `<row/>` element to avoid adding a new `<row/>` and `<table/>` for each solitary `<cell/>`.
If the `<cell/>` element has a tail, it will be moved to the `<table/>` element.


### Example
Before transformation:
```xml
<div>
  <p>
    <table>
      <cell>text</cell>
    </table>
    <table>
      <cell>text2</cell>
      <cell>text3</cell>
    </table>
  </p>
  <cell/>
  <p>
    <cell>new table</cell>tail
  </p>
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
    </table>
    <table>
      <row>
        <cell>text2</cell>
        <cell>text3</cell>
      </row>
    </table>
  </p>
  <table>
    <row>
      <cell/>
    </row>
  </table>
  <p>
    <table>
      <row>
        <cell>new table</cell>
      </row>
    </table>tail
  </p>
</div>
```
