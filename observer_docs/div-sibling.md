## div-sibling
Find `<table/>`, `<quote/>`, `<list/>`, `<p/>`, `<head/>`, or `<ab/>` elements that are a following sibling of a `<div/>` element and add a new `<div/>` wrapping the target element. Multiple adjacent elements following the same `<div/>` element will be gathered under the same parent to avoid adding a new `<div/>` for each infringing element.

If the target element is empty, it will be removed instead.

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
  <p/>
  <p>text</p>
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
    <p>text</p>
  </div>
</div>
```
