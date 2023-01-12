## div-sibling
Find `<table/>`, `<quote/>` or `<list/>` elements that are a following sibling of  `<div/>` elements and add a new `<div/>` wrapping the `<table/>`, `<quote/>`, or `<list/>` element. Multiple adjacent elements following the same `<div/>` elements will be gathered under the same parent to avoid adding a new `<div/>` for each infringing element.

### Example
Before transformation:
```xml
<div>
  <div>
    <p>text</p>
  </div>
  <table>
    <row>
      <cell>text</cell>
    </row>
  </table>
</div>
```

After transformation:
```xml
<div>
  <div>
    <p>text</p>
  </div>
  <div> <!-- insert new <div> here -->
    <table>
      <row>
        <cell>text</cell>
      </row>
    </table>
  </div>
</div>
```
